from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection URL for local MongoDB instance
MONGODB_URL = 'mongodb://localhost:27017'

# Create the MongoDB client
client = AsyncIOMotorClient(MONGODB_URL)

# Select your database
db = client['student_management_system']

# Define a function to get the database instance
async def get_db():
    try:
        yield db
    finally:
        pass

