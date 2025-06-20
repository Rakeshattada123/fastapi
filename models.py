from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class BookBase(BaseModel):
    """Base book model with common fields"""
    title: str = Field(..., min_length=1, max_length=200, description="Title of the book")
    author: str = Field(..., min_length=1, max_length=100, description="Author of the book")
    ISBN: str = Field(..., min_length=10, max_length=17, description="ISBN of the book")
    genre: str = Field(..., min_length=1, max_length=50, description="Genre of the book")
    publication_year: int = Field(..., ge=1000, le=2024, description="Publication year of the book")

    @validator('ISBN')
    def validate_isbn(cls, v):
        """Validate ISBN format (basic validation)"""
        # Remove hyphens and spaces
        isbn = v.replace('-', '').replace(' ', '')
        
        # Check if it's 10 or 13 digits
        if not (len(isbn) == 10 or len(isbn) == 13):
            raise ValueError('ISBN must be 10 or 13 characters long')
        
        # Check if all characters are digits (except last character of ISBN-10 can be X)
        if len(isbn) == 10:
            if not (isbn[:-1].isdigit() and (isbn[-1].isdigit() or isbn[-1].upper() == 'X')):
                raise ValueError('Invalid ISBN-10 format')
        else:  # ISBN-13
            if not isbn.isdigit():
                raise ValueError('Invalid ISBN-13 format')
        
        return v

    @validator('title', 'author', 'genre')
    def validate_strings(cls, v):
        """Validate string fields are not just whitespace"""
        if not v.strip():
            raise ValueError('Field cannot be empty or just whitespace')
        return v.strip()

class BookCreate(BookBase):
    """Model for creating a new book"""
    pass

class BookUpdate(BaseModel):
    """Model for updating a book (all fields optional)"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Title of the book")
    author: Optional[str] = Field(None, min_length=1, max_length=100, description="Author of the book")
    ISBN: Optional[str] = Field(None, min_length=10, max_length=17, description="ISBN of the book")
    genre: Optional[str] = Field(None, min_length=1, max_length=50, description="Genre of the book")
    publication_year: Optional[int] = Field(None, ge=1000, le=2024, description="Publication year of the book")

    @validator('ISBN')
    def validate_isbn(cls, v):
        """Validate ISBN format if provided"""
        if v is None:
            return v
        
        # Remove hyphens and spaces
        isbn = v.replace('-', '').replace(' ', '')
        
        # Check if it's 10 or 13 digits
        if not (len(isbn) == 10 or len(isbn) == 13):
            raise ValueError('ISBN must be 10 or 13 characters long')
        
        # Check if all characters are digits (except last character of ISBN-10 can be X)
        if len(isbn) == 10:
            if not (isbn[:-1].isdigit() and (isbn[-1].isdigit() or isbn[-1].upper() == 'X')):
                raise ValueError('Invalid ISBN-10 format')
        else:  # ISBN-13
            if not isbn.isdigit():
                raise ValueError('Invalid ISBN-13 format')
        
        return v

    @validator('title', 'author', 'genre')
    def validate_strings(cls, v):
        """Validate string fields are not just whitespace if provided"""
        if v is not None and not v.strip():
            raise ValueError('Field cannot be empty or just whitespace')
        return v.strip() if v is not None else v

class BookResponse(BookBase):
    """Model for book responses (includes ID)"""
    id: str = Field(..., description="Unique identifier of the book")

    class Config:
        # Allow population by field name for MongoDB _id conversion
        allow_population_by_field_name = True
        # Example for API documentation
        schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "ISBN": "978-0-7432-7356-5",
                "genre": "Fiction",
                "publication_year": 1925
            }
        }
