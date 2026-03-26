from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. User Model (dengan roles)
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('instructor', 'Instructor'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

# 2. Category Model (Self-referencing)
class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

# --- CUSTOM MANAGERS UNTUK OPTIMASI QUERY (25% Poin) ---
class CourseManager(models.Manager):
    def for_listing(self):
        # select_related untuk ForeignKey (1-to-1/Many-to-1)
        # prefetch_related untuk Reverse ForeignKey/Many-to-Many
        return self.select_related('instructor', 'category').prefetch_related('lesson_set')

class EnrollmentManager(models.Manager):
    def for_student_dashboard(self):
        return self.select_related('course', 'student').prefetch_related('progress_set__lesson')

# 3. Course Model
class Course(models.Model):
    title = models.CharField(max_length=200)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_taught')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses')
    
    objects = CourseManager() # Pasang custom manager

    def __str__(self):
        return self.title

# 4. Lesson Model (dengan ordering)
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lesson_set')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order'] # Mengurutkan berdasarkan field order otomatis

    def __str__(self):
        return f"{self.course.title} - {self.title}"

# 5. Enrollment Model (dengan unique constraint)
class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    objects = EnrollmentManager()

    class Meta:
        unique_together = ('student', 'course') # 1 user hanya bisa daftar 1 course yang sama 1 kali

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"

# 6. Progress Model
class Progress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='progress_set')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('enrollment', 'lesson')

    def __str__(self):
        status = "Done" if self.is_completed else "Pending"
        return f"{self.enrollment.student.username} - {self.lesson.title} ({status})"

# Create your models here.
