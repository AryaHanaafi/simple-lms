from ninja import NinjaAPI, Router
from django.contrib.auth.hashers import make_password, check_password
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
import jwt
from django.conf import settings
from .models import User, Course, Enrollment, Progress, Lesson
from .schemas import *
from .security import JWTAuth, create_tokens, is_admin, is_instructor, is_student

api = NinjaAPI(title="Simple LMS API", description="API untuk Sistem Manajemen Pembelajaran", version="1.0.0")

auth_router = Router()
courses_router = Router()
enroll_router = Router()

# ================= AUTHENTICATION =================
@auth_router.post("/register", response=UserOut)
def register(request, payload: RegisterSchema):
    if User.objects.filter(username=payload.username).exists():
        raise HttpError(400, "Username sudah digunakan")
    user = User.objects.create(
        username=payload.username, email=payload.email,
        password=make_password(payload.password), role=payload.role
    )
    return user

@auth_router.post("/login", response=TokenSchema)
def login(request, payload: LoginSchema):
    user = User.objects.filter(username=payload.username).first()
    if not user or not check_password(payload.password, user.password):
        raise HttpError(401, "Username atau password salah")
    return create_tokens(user.id)

@auth_router.post("/refresh", response=TokenSchema)
def refresh(request, refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
        if payload.get("type") != "refresh": raise HttpError(401, "Invalid token type")
        return create_tokens(payload["user_id"])
    except Exception:
        raise HttpError(401, "Token refresh tidak valid")

@auth_router.get("/me", auth=JWTAuth(), response=UserOut)
def get_me(request):
    return request.user

@auth_router.put("/me", auth=JWTAuth(), response=UserOut)
def update_profile(request, payload: UserUpdate):
    user = request.user
    if payload.email:
        user.email = payload.email
        user.save()
    return user

# ================= COURSES =================
@courses_router.get("", response=list[CourseOut])
def list_courses(request):
    return Course.objects.select_related('instructor').all()

@courses_router.get("/{id}", response=CourseOut)
def get_course(request, id: int):
    return get_object_or_404(Course, id=id)

@courses_router.post("", auth=JWTAuth(), response=CourseOut)
def create_course(request, payload: CourseCreate):
    is_instructor(request)
    course = Course.objects.create(title=payload.title, category_id=payload.category_id, instructor=request.user)
    return course

@courses_router.patch("/{id}", auth=JWTAuth(), response=CourseOut)
def update_course(request, id: int, payload: CourseUpdate):
    is_instructor(request)
    course = get_object_or_404(Course, id=id)
    # Ownership Validation
    if course.instructor != request.user and request.user.role != 'admin':
        raise HttpError(403, "Anda bukan pemilik course ini")
    
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(course, attr, value)
    course.save()
    return course

@courses_router.delete("/{id}", auth=JWTAuth())
def delete_course(request, id: int):
    is_admin(request)
    course = get_object_or_404(Course, id=id)
    course.delete()
    return {"success": True, "message": "Course berhasil dihapus"}

# ================= ENROLLMENTS =================
@enroll_router.post("", auth=JWTAuth())
def enroll_course(request, payload: EnrollmentCreate):
    is_student(request)
    course = get_object_or_404(Course, id=payload.course_id)
    enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)
    if not created: raise HttpError(400, "Sudah terdaftar di course ini")
    return {"success": True, "message": "Berhasil mendaftar"}

@enroll_router.get("/my-courses", auth=JWTAuth())
def my_courses(request):
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    return [{"id": e.course.id, "title": e.course.title} for e in enrollments]

@enroll_router.post("/{id}/progress", auth=JWTAuth())
def update_progress(request, id: int, payload: ProgressUpdate):
    is_student(request)
    enrollment = get_object_or_404(Enrollment, id=id, student=request.user)
    lesson = get_object_or_404(Lesson, id=payload.lesson_id, course=enrollment.course)
    progress, _ = Progress.objects.update_or_create(
        enrollment=enrollment, lesson=lesson, defaults={"is_completed": payload.is_completed}
    )
    return {"success": True, "status": progress.is_completed}

# Register Routers
api.add_router("/auth", auth_router, tags=["Authentication"])
api.add_router("/courses", courses_router, tags=["Courses"])
api.add_router("/enrollments", enroll_router, tags=["Enrollments"])