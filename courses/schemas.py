from ninja import Schema, ModelSchema
from pydantic import EmailStr
from typing import Optional
from .models import User, Course

# --- AUTH SCHEMAS ---
class RegisterSchema(Schema):
    username: str
    email: EmailStr
    password: str
    role: str = "student"

class LoginSchema(Schema):
    username: str
    password: str

class TokenSchema(Schema):
    access_token: str
    refresh_token: str

class UserOut(ModelSchema):
    class Config:
        model = User
        model_fields = ['id', 'username', 'email', 'role']

class UserUpdate(Schema):
    email: Optional[EmailStr] = None

# --- COURSE SCHEMAS ---
class CourseOut(ModelSchema):
    instructor_name: str
    class Config:
        model = Course
        model_fields = ['id', 'title']
    
    @staticmethod
    def resolve_instructor_name(obj):
        return obj.instructor.username

class CourseCreate(Schema):
    title: str
    category_id: int

class CourseUpdate(Schema):
    title: Optional[str] = None
    category_id: Optional[int] = None

# --- ENROLLMENT SCHEMAS ---
class EnrollmentCreate(Schema):
    course_id: int

class ProgressUpdate(Schema):
    lesson_id: int
    is_completed: bool