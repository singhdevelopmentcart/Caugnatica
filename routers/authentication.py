from ..hashing import Hash
from .. import database
from ..schemas import user_schema
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status, HTTPException
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
import jwt

router = APIRouter(
    prefix="/v1/users",
    tags=['Authentication']
)

get_db = database.get_db

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480

#----------------user login---------------------
@router.post('/login', response_model= user_schema.LoginResponse)
async def login(request:OAuth2PasswordRequestForm = Depends(), db: AsyncIOMotorClient = Depends(get_db)):
    if len(request.username)==0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
                                'status': 422, 'message': 'username is empty'})
    user = ''
    table_name = ''
    teacher_data = await db["user_model"].find_one({"email": request.username})
    if teacher_data:
        user = teacher_data
        table_name = "user_model"
        
    student_data = await db["student_model"].find_one({"email": request.username})
    if student_data:
        user = student_data
        table_name = "student_model"

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'status': 401, 'message': "Incorrect Email"})
    if not Hash.verify(user["password"], request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'status': 401, 'message': "Incorrect Password"})

    payload = {'email': user['email'], 'exp': datetime.utcnow() + timedelta(minutes=480)}
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256') 
    await db[table_name].update_one({"_id": user["_id"]}, {"$set": {"auth": token, "last_login": datetime.now(), "updated_at": datetime.now()}})  

    updated_user = await db[table_name].find_one({"email": request.username})
    return user_schema.LoginResponse(detail={"status": 200, "messgae": "Login successful"}, auth=token, data = updated_user)

