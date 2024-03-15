from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class StudentTeacherRegistration(BaseModel):
    first_name: str
    last_name: Optional[str]
    email: str
    encrypted_password: str
    last_login_time: Optional[datetime]
    created_at: datetime
    updated_at: datetime



