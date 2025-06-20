import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import asyncio

# MongoDB configuration
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "library_management")

class Database:
    client: AsyncIOMotorClient = None
    database = None

# Global database instance
database = Database()

async def get_database():
    """Get database instance"""
    return database.database

async def connect_to_mongo():
    """Create database connection"""
    try:
        database.client = AsyncIOMotorClient(MONGODB_URL)
        database.database = database.client[DATABASE_NAME]
        
        # Test the connection
        await database.client.admin.command('ping')
        print(f"Successfully connected to MongoDB at {MONGODB_URL}")
        print(f"Using database: {DATABASE_NAME}")
        
        # Create indexes for better performance
        await create_indexes()
        
        return database.database
    except ConnectionFailure as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise e
    except Exception as e:
        print(f"An error occurred while connecting to MongoDB: {e}")
        raise e

async def close_mongo_connection():
    """Close database connection"""
    if database.client:
        database.client.close()
        print("Disconnected from MongoDB")

async def create_indexes():
    """Create database indexes for better performance"""
    try:
        # Create index on ISBN for uniqueness and faster lookups
        await database.database.books.create_index("ISBN", unique=True)
        
        # Create text index for search functionality
        await database.database.books.create_index([
            ("title", "text"),
            ("author", "text")
        ])
        
        # Create indexes for filtering
        await database.database.books.create_index("genre")
        await database.database.books.create_index("publication_year")
        
        print("Database indexes created successfully")
    except Exception as e:
        print(f"Error creating indexes: {e}")

# Initialize database connection
async def init_db():
    """Initialize database connection"""
    return await connect_to_mongo()

if __name__ == "__main__":
    # Test database connection
    async def test_connection():
        try:
            db = await init_db()
            print("Database connection test successful!")
            await close_mongo_connection()
        except Exception as e:
            print(f"Database connection test failed: {e}")
    
    asyncio.run(test_connection())
