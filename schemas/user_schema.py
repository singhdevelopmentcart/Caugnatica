from typing import List, Optional
from pydantic import BaseModel, validator
from fastapi.exceptions import HTTPException
from fastapi import status
from datetime import datetime, date
import re
from enum import Enum


class RoleEnum(str, Enum):
    student = "student"
    teacher = "teacher"

class StudentTeacherRegistrationBase(BaseModel):
    first_name: str
    last_name: Optional[str]
    email: str
    password: str
    role: RoleEnum

    class Config():
        from_attributes =True

    @validator('first_name')
    def first_name_empty(value):
        if len(value) == 0:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={'status': 422, 'message': "First name can not be empty"})
        return value
    
    # @validator('last_name')
    # def last_name_empty(value):
    #     if len(value) == 0:
    #         raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={'status': 422, 'message': "Last name can not be empty"})
    #     return value

    @validator('email')
    def email_empty(value):
        if len(value) == 0:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail= {'status':422,'message':"email can not be empty"})
        return value

    @validator('email')
    def email_validation(value):
        regex = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        if (re.fullmatch(regex, value)):
            print("valid mail")
        else:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
                                'status': 422, 'message': "Enter valid Email id"})
        return value

    @validator('password')
    def password_empty(value):
        if len(value) == 0:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail= {'status':422,'message':"password can not be empty"})
        return value

    @validator('password')
    def password_validation(value):
        regex = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$'
        if (re.fullmatch(regex, value)):
            print("valid password")
        else:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
                                'status': 422, 'message': "Password should be Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character"})
        return value

    @validator('role')
    def check_role(value):
        if len(value) == 0:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={'status': 422, 'message': "role can not be empty"})
        return value
    
    @validator("role")
    def role_must_be_valid(v):
        if v not in RoleEnum:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={'status': 422, 'message': "Invalid role. Must be either 'student' or 'teacher'"})
        return v

class LoginResponseBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    role: str
    last_login: Optional[datetime]
    created_at : datetime

    class Config():
        from_attributes =True

class LoginResponse(BaseModel):
    detail: dict
    auth : str
    data: LoginResponseBase

    class Config():
        from_attributes =True

#---------forget password--------------
class ForgetPassword(BaseModel):
    email: str
    class Config():
        from_attributes = True

    @validator('email')
    def email_empty(value):
        if len(value) == 0:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail= {'status':422,'message':"email can not be empty"})
        return value

    @validator('email')
    def email_validation(value):
        regex = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        if (re.fullmatch(regex, value)):
            print("valid mail")
        else:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
                                'status': 422, 'message': "Enter valid Email id"})
        return value