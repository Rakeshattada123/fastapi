# Library Management System API

A comprehensive FastAPI-based Library Management System with MongoDB integration that provides full CRUD operations, search functionality, filtering, and analytics for managing library books.

## Features

### Core CRUD Operations
- ✅ **Create** a new book
- ✅ **Read** book by ID or get all books with pagination
- ✅ **Update** book information
- ✅ **Delete** book from library

### Advanced Features
- 🔍 **Search** books by title or author
- 🎯 **Filter** books by genre and publication year
- 📊 **Count** total books in library
- 📈 **Analytics** - count books per genre
- ✅ **Data Validation** with Pydantic models
- 🚀 **Async/Await** support for better performance
- 📚 **Auto-generated API documentation**

## Technology Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **MongoDB** - NoSQL database for flexible document storage
- **Motor** - Async MongoDB driver for Python
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - ASGI server for running the application

## Project Structure

\`\`\`
library-management-api/
├── main.py              # Main FastAPI application
├── models.py            # Pydantic models for data validation
├── database.py          # MongoDB connection and configuration
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables example
└── README.md           # This file
\`\`\`

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- MongoDB (local installation or MongoDB Atlas)

### 1. Clone or Download the Project
\`\`\`bash
# If you have the code in a repository
git clone <repository-url>
cd library-management-api

# Or create a new directory and copy the files
mkdir library-management-api
cd library-management-api
\`\`\`

### 2. Create Virtual Environment
\`\`\`bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\\Scripts\\activate
# On macOS/Linux:
source venv/bin/activate
\`\`\`

### 3. Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. MongoDB Setup

#### Option A: Local MongoDB
1. Install MongoDB Community Edition from [MongoDB Official Website](https://www.mongodb.com/try/download/community)
2. Start MongoDB service:
   \`\`\`bash
   # On Windows (if installed as service):
   net start MongoDB
   
   # On macOS:
   brew services start mongodb-community
   
   # On Linux:
   sudo systemctl start mongod
   \`\`\`

#### Option B: MongoDB Atlas (Cloud)
1. Create a free account at [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a new cluster
3. Get your connection string
4. Whitelist your IP address

### 5. Environment Configuration
\`\`\`bash
# Copy the example environment file
cp .env.example .env

# Edit .env file with your MongoDB configuration
# For local MongoDB:
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=library_management

# For MongoDB Atlas:
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=library_management
\`\`\`

### 6. Run the Application
\`\`\`bash
# Start the FastAPI server
python main.py

# Or use uvicorn directly:
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
\`\`\`

The API will be available at:
- **Application**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## API Endpoints

### Core CRUD Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/books/` | Create a new book |
| GET | `/books/{book_id}` | Get book by ID |
| PUT | `/books/{book_id}` | Update book by ID |
| DELETE | `/books/{book_id}` | Delete book by ID |
| GET | `/books/` | Get all books (with pagination) |

### Search & Filter Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/books/search/` | Search books by title or author |
| GET | `/books/filter/` | Filter books by genre and/or year |

### Analytics Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/books/count/total` | Count total books |
| GET | `/books/count/by-genre` | Count books per genre |

### Utility Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |

## Book Schema

\`\`\`json
{
  "title": "string",
  "author": "string", 
  "ISBN": "string",
  "genre": "string",
  "publication_year": "integer"
}
\`\`\`

### Field Validations
- **title**: 1-200 characters, required
- **author**: 1-100 characters, required
- **ISBN**: 10-17 characters, must be valid ISBN-10 or ISBN-13 format
- **genre**: 1-50 characters, required
- **publication_year**: Integer between 1000-2024

## Usage Examples

### 1. Create a Book
\`\`\`bash
curl -X POST "http://localhost:8000/books/" \\
  -H "Content-Type: application/json" \\
  -d '{
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "ISBN": "978-0-7432-7356-5",
    "genre": "Fiction",
    "publication_year": 1925
  }'
\`\`\`

### 2. Search Books
\`\`\`bash
curl "http://localhost:8000/books/search/?query=gatsby"
\`\`\`

### 3. Filter Books
\`\`\`bash
curl "http://localhost:8000/books/filter/?genre=Fiction&publication_year=1925"
\`\`\`

### 4. Get Book Count by Genre
\`\`\`bash
curl "http://localhost:8000/books/count/by-genre"
\`\`\`

## Error Handling

The API provides comprehensive error handling with appropriate HTTP status codes:

- **400 Bad Request**: Invalid input data or validation errors
- **404 Not Found**: Book not found
- **500 Internal Server Error**: Server-side errors

Example error response:
\`\`\`json
{
  "detail": "Book with this ISBN already exists"
}
\`\`\`

## Performance Features

- **Database Indexes**: Automatic creation of indexes for better query performance
- **Async Operations**: All database operations are asynchronous
- **Pagination**: Built-in pagination for list endpoints
- **Connection Pooling**: Efficient database connection management

## Testing the API

### Using the Interactive Documentation
1. Open http://localhost:8000/docs
2. Click on any endpoint to expand it
3. Click "Try it out" to test the endpoint
4. Fill in the required parameters
5. Click "Execute" to send the request

### Using curl or Postman
You can test all endpoints using curl commands or import the API into Postman using the OpenAPI specification available at http://localhost:8000/openapi.json

## Troubleshooting

### Common Issues

1. **MongoDB Connection Error**
   - Ensure MongoDB is running
   - Check your connection string in `.env`
   - Verify network connectivity for Atlas

2. **Port Already in Use**
   - Change the port in the run command: `uvicorn main:app --port 8001`

3. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Activate your virtual environment

4. **Database Permission Issues**
   - For MongoDB Atlas, ensure your IP is whitelisted
   - Check database user permissions

### Logs and Debugging
- The application logs connection status and errors to the console
- Use the `/health` endpoint to check database connectivity
- Enable debug mode by adding `--log-level debug` to the uvicorn command

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.
\`\`\`

## Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the API documentation at `/docs`
3. Check MongoDB connection and logs
4. Ensure all dependencies are properly installed

---

**Happy coding! 📚✨**
\`\`\`

```python file="scripts/test_api.py"
"""
Test script to verify the Library Management System API functionality
Run this after starting the FastAPI server to test all endpoints
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

class APITester:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = None
        self.created_book_id = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def make_request(self, method: str, endpoint: str, data: Dict[Any, Any] = None, params: Dict[str, Any] = None):
        """Make HTTP request and return response"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                async with self.session.get(url, params=params) as response:
                    return await response.json(), response.status
            elif method.upper() == "POST":
                async with self.session.post(url, json=data) as response:
                    return await response.json(), response.status
            elif method.upper() == "PUT":
                async with self.session.put(url, json=data) as response:
                    return await response.json(), response.status
            elif method.upper() == "DELETE":
                async with self.session.delete(url) as response:
                    if response.status == 200:
                        return await response.json(), response.status
                    else:
                        return {"error": "Delete failed"}, response.status
        except Exception as e:
            return {"error": str(e)}, 500

    async def test_health_check(self):
        """Test health check endpoint"""
        print("🏥 Testing health check...")
        response, status = await self.make_request("GET", "/health")
        print(f"Status: {status}")
        print(f"Response: {json.dumps(response, indent=2)}")
        print("-" * 50)

    async def test_create_book(self):
        """Test creating a new book"""
        print("📚 Testing book creation...")
        book_data = {
            "title": "Test Book for API",
            "author": "API Tester",
            "ISBN": "978-0-123456-78-9",
            "genre": "Technology",
            "publication_year": 2023
        }
        
        response, status = await self.make_request("POST", "/books/", data=book_data)
        print(f"Status: {status}")
        print(f"Response: {json.dumps(response, indent=2)}")
        
        if status == 201 and "id" in response:
            self.created_book_id = response["id"]
            print(f"✅ Book created successfully with ID: {self.created_book_id}")
        else:
            print("❌ Failed to create book")
        
        print("-" * 50)

    async def test_get_book(self):
        """Test getting a book by ID"""
        if not self.created_book_id:
            print("⚠️ Skipping get book test - no book ID available")
            return
        
        print(f"📖 Testing get book by ID: {self.created_book_id}")
        response, status = await self.make_request("GET", f"/books/{self.created_book_id}")
        print(f"Status: {status}")
        print(f"Response: {json.dumps(response, indent=2)}")
        print("-" * 50)

    async def test_update_book(self):
        """Test updating a book"""
        if not self.created_book_id:
            print("⚠️ Skipping update book test - no book ID available")
            return
        
        print(f"✏️ Testing book update for ID: {self.created_book_id}")
        update_data = {
            "title": "Updated Test Book",
            "genre": "Updated Technology"
        }
        
        response, status = await self.make_request("PUT", f"/books/{self.created_book_id}", data=update_data)
        print(f"Status: {status}")
        print(f"Response: {json.dumps(response, indent=2)}")
        print("-" * 50)

    async def test_search_books(self):
        """Test searching books"""
        print("🔍 Testing book search...")
        params = {"query": "Test"}
        response, status = await self.make_request("GET", "/books/search/", params=params)
        print(f"Status: {status}")
        print(f"Response: {json.dumps(response, indent=2)}")
        print("-" * 50)

    async def test_filter_books(self):
        """Test filtering books"""
        print("🎯 Testing book filtering...")
        params = {"genre": "Technology"}
        response, status = await self.make_request("GET", "/books/filter/", params=params)
        print(f"Status: {status}")
        print(f"Response: {json.dumps(response, indent=2)}")
        print("-" * 50)

    async def test_count_total_books(self):
        """Test counting total books"""
        print("🔢 Testing total book count...")
        response, status = await self.make_request("GET", "/books/count/total")
        print(f"Status: {status}")
        print(f"Response: {json.dumps(response, indent=2)}")
        print("-" * 50)

    async def test_count_books_by_genre(self):
        """Test counting books by genre"""
        print("📊 Testing book count by genre...")
        response, status = await self.make_request("GET", "/books/count/by-genre")
        print(f"Status: {status}")
        print(f"Response: {json.dumps(response, indent=2)}")
        print("-" * 50)

    async def test_get_all_books(self):
        """Test getting all books"""
        print("📚 Testing get all books...")
        params = {"skip": 0, "limit": 5}
        response, status = await self.make_request("GET", "/books/", params=params)
        print(f"Status: {status}")
        print(f"Response: {json.dumps(response, indent=2)}")
        print("-" * 50)

    async def test_delete_book(self):
        """Test deleting a book"""
        if not self.created_book_id:
            print("⚠️ Skipping delete book test - no book ID available")
            return
        
        print(f"🗑️ Testing book deletion for ID: {self.created_book_id}")
        response, status = await self.make_request("DELETE", f"/books/{self.created_book_id}")
        print(f"Status: {status}")
        print(f"Response: {json.dumps(response, indent=2)}")
        print("-" * 50)

    async def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting Library Management System API Tests")
        print("=" * 60)
        
        # Test all endpoints
        await self.test_health_check()
        await self.test_create_book()
        await self.test_get_book()
        await self.test_update_book()
        await self.test_get_all_books()
        await self.test_search_books()
        await self.test_filter_books()
        await self.test_count_total_books()
        await self.test_count_books_by_genre()
        await self.test_delete_book()
        
        print("✅ All tests completed!")
        print("=" * 60)

async def main():
    """Main function to run the tests"""
    print("Make sure your FastAPI server is running at http://localhost:8000")
    print("Starting tests in 3 seconds...")
    await asyncio.sleep(3)
    
    async with APITester() as tester:
        await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
