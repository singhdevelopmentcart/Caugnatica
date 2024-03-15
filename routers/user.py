from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from ..import database
from ..repository import user
from ..validation import check_mail
from ..schemas import user_schema

router = APIRouter(
    prefix="/v1/users",
    tags=['users']
)

get_db = database.get_db

# --------- Teacher and Student registration-----
@router.post('', status_code=status.HTTP_201_CREATED)
async def register_student_or_teacher(request: user_schema.StudentTeacherRegistrationBase, db: AsyncIOMotorClient = Depends(get_db)):
    if await check_mail(request, db):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"status": 409, "message": "Email already exists"})
    return await user.create_user_or_teacher(request, db)
    
# --------Forget Password ------------
@router.post("/forget-password", status_code=status.HTTP_202_ACCEPTED)
async def forget_password(request: user_schema.ForgetPassword, db: AsyncIOMotorClient = Depends(get_db)):
    return await user.forget_password_function(request, db)
