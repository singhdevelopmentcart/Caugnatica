from datetime import datetime
from ..models import user_models
from ..hashing import Hash
from ..schemas import user_schema
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import string
import secrets
 
#---------------Teacher and Student registration-------------------------------
async def create_user_or_teacher(request: user_schema.StudentTeacherRegistrationBase, db: AsyncIOMotorClient):
    try:
        if request.role == 'admin':
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'status': 403, 'message': "admin user signup is not allowed."})
        if request.role == 'teacher':  
            user_data = {
                "first_name": request.first_name,
                "last_name": request.last_name,
                "email": request.email,
                "username": (request.first_name)+(request.last_name),
                "date_of_joining":datetime.now(),
                "password": Hash.bcrypt(request.password),
                "role": request.role,
                "email_verified": False,
                "created_at": datetime.now()
            }
            result = await db['user_model'].insert_one(user_data)
        if request.role == 'student':
            user_data = {
                "first_name": request.first_name,
                "last_name": request.last_name,
                "email": request.email,
                "username": (request.first_name)+(request.last_name),
                "registered": True,
                "registered_date": datetime.now(),
                "password": Hash.bcrypt(request.password),
                "role": request.role,
                "email_verified": False,
                "created_at": datetime.now()
            }
            result = await db['student_model'].insert_one(user_data)
        if result:
            return JSONResponse(status_code=201, content={"detail": {"status": 201, "message": "User created successfully."}, "data": {"email": request.email}})
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": {"status": 500, "message": f"Failed to register user: {str(e)}"}})

#-------------Forget Password-----------------------------------------
async def forget_password_function(request: user_schema.ForgetPassword, db: AsyncIOMotorClient):
    user = await db['org_users'].find_one({"email": request.email})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'status': 404, 'message': "User not found"})

    # Generate a random password using the defined characters
    characters = string.ascii_letters+ "@#$&" + string.digits 
    length = 9
    new_password = ''.join(secrets.choice(characters) for _ in range(length))
    print("password-->>", new_password)
    await db['org_users'].update_one({"_id": ObjectId(user["_id"])}, {"$set": {"encrypted_password": Hash.bcrypt(new_password), "updated_at": datetime.now()}})

    await send_email(request.email, "Password Reset", email_content)

    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"detail": {"status": 202, "message": "Password reset successfully"}})