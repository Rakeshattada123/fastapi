from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import Optional, List
import os
from contextlib import asynccontextmanager

from models import BookCreate, BookUpdate, BookResponse
from database import get_database

# Global database variable
db = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global db
    db = await get_database()
    yield
    # Shutdown - MongoDB client will be closed automatically

app = FastAPI(
    title="Library Management System",
    description="A comprehensive API for managing library books with CRUD operations, search, filter, and analytics",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    """Welcome endpoint"""
    return {"message": "Welcome to Library Management System API", "docs": "/docs"}

# CRUD Operations

@app.post("/books/", response_model=BookResponse, status_code=201)
async def create_book(book: BookCreate):
    """Create a new book in the library"""
    try:
        # Check if book with same ISBN already exists
        existing_book = await db.books.find_one({"ISBN": book.ISBN})
        if existing_book:
            raise HTTPException(status_code=400, detail="Book with this ISBN already exists")
        
        book_dict = book.dict()
        result = await db.books.insert_one(book_dict)
        
        # Retrieve the created book
        created_book = await db.books.find_one({"_id": result.inserted_id})
        created_book["id"] = str(created_book["_id"])
        del created_book["_id"]
        
        return BookResponse(**created_book)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error creating book: {str(e)}")

@app.get("/books/{book_id}", response_model=BookResponse)
async def get_book(book_id: str):
    """Get a book by its ID"""
    try:
        if not ObjectId.is_valid(book_id):
            raise HTTPException(status_code=400, detail="Invalid book ID format")
        
        book = await db.books.find_one({"_id": ObjectId(book_id)})
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        book["id"] = str(book["_id"])
        del book["_id"]
        return BookResponse(**book)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error retrieving book: {str(e)}")

@app.put("/books/{book_id}", response_model=BookResponse)
async def update_book(book_id: str, book_update: BookUpdate):
    """Update a book by its ID"""
    try:
        if not ObjectId.is_valid(book_id):
            raise HTTPException(status_code=400, detail="Invalid book ID format")
        
        # Check if book exists
        existing_book = await db.books.find_one({"_id": ObjectId(book_id)})
        if not existing_book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        # Check if ISBN is being updated and if it conflicts with another book
        update_data = book_update.dict(exclude_unset=True)
        if "ISBN" in update_data:
            isbn_conflict = await db.books.find_one({
                "ISBN": update_data["ISBN"],
                "_id": {"$ne": ObjectId(book_id)}
            })
            if isbn_conflict:
                raise HTTPException(status_code=400, detail="Another book with this ISBN already exists")
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        result = await db.books.update_one(
            {"_id": ObjectId(book_id)},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="No changes made to the book")
        
        # Retrieve updated book
        updated_book = await db.books.find_one({"_id": ObjectId(book_id)})
        updated_book["id"] = str(updated_book["_id"])
        del updated_book["_id"]
        
        return BookResponse(**updated_book)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error updating book: {str(e)}")

@app.delete("/books/{book_id}")
async def delete_book(book_id: str):
    """Delete a book by its ID"""
    try:
        if not ObjectId.is_valid(book_id):
            raise HTTPException(status_code=400, detail="Invalid book ID format")
        
        result = await db.books.delete_one({"_id": ObjectId(book_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Book not found")
        
        return {"message": "Book deleted successfully"}
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error deleting book: {str(e)}")

@app.get("/books/", response_model=List[BookResponse])
async def get_all_books(
    skip: int = Query(0, ge=0, description="Number of books to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of books to return")
):
    """Get all books with pagination"""
    try:
        cursor = db.books.find().skip(skip).limit(limit)
        books = await cursor.to_list(length=limit)
        
        for book in books:
            book["id"] = str(book["_id"])
            del book["_id"]
        
        return [BookResponse(**book) for book in books]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving books: {str(e)}")

# Additional Operations

@app.get("/books/search/", response_model=List[BookResponse])
async def search_books(
    query: str = Query(..., min_length=1, description="Search query for title or author"),
    skip: int = Query(0, ge=0, description="Number of books to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of books to return")
):
    """Search books by title or author"""
    try:
        search_filter = {
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"author": {"$regex": query, "$options": "i"}}
            ]
        }
        
        cursor = db.books.find(search_filter).skip(skip).limit(limit)
        books = await cursor.to_list(length=limit)
        
        for book in books:
            book["id"] = str(book["_id"])
            del book["_id"]
        
        return [BookResponse(**book) for book in books]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching books: {str(e)}")

@app.get("/books/filter/", response_model=List[BookResponse])
async def filter_books(
    genre: Optional[str] = Query(None, description="Filter by genre"),
    publication_year: Optional[int] = Query(None, ge=1000, le=2024, description="Filter by publication year"),
    skip: int = Query(0, ge=0, description="Number of books to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of books to return")
):
    """Filter books by genre and/or publication year"""
    try:
        filter_dict = {}
        
        if genre:
            filter_dict["genre"] = {"$regex": genre, "$options": "i"}
        
        if publication_year:
            filter_dict["publication_year"] = publication_year
        
        if not filter_dict:
            raise HTTPException(status_code=400, detail="At least one filter parameter is required")
        
        cursor = db.books.find(filter_dict).skip(skip).limit(limit)
        books = await cursor.to_list(length=limit)
        
        for book in books:
            book["id"] = str(book["_id"])
            del book["_id"]
        
        return [BookResponse(**book) for book in books]
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error filtering books: {str(e)}")

@app.get("/books/count/total")
async def count_total_books():
    """Count total number of books in the library"""
    try:
        total_count = await db.books.count_documents({})
        return {"total_books": total_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error counting books: {str(e)}")

@app.get("/books/count/by-genre")
async def count_books_by_genre():
    """Count number of books per genre"""
    try:
        pipeline = [
            {
                "$group": {
                    "_id": "$genre",
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {"count": -1}
            }
        ]
        
        cursor = db.books.aggregate(pipeline)
        genre_counts = await cursor.to_list(length=None)
        
        # Format the response
        result = {}
        for item in genre_counts:
            genre = item["_id"] if item["_id"] else "Unknown"
            result[genre] = item["count"]
        
        return {"books_per_genre": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error counting books by genre: {str(e)}")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        await db.books.find_one()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "database": "disconnected", "error": str(e)}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
