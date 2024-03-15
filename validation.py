from .models import user_models
from .schemas import user_schema
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException

app = FastAPI()

async def get_current_active_user(request: user_schema.StudentTeacherRegistrationBase, db: AsyncIOMotorClient):
    user = await db['org_users'].find_one({"email": request.email, "is_active": True})
    return user


async def check_mail(request: user_schema.StudentTeacherRegistrationBase, db: AsyncIOMotorClient):
    if request.role == 'teacher': 
        user = await db['user_model'].find_one({"email": request.email})
    if request.role == 'student': 
        user = await db['student_model'].find_one({"email": request.email})
    return user
