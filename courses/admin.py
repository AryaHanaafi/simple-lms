from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Course, Lesson, Enrollment, Progress

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    # Menambahkan field role ke form edit admin
    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    list_filter = ('parent',)

# Menggunakan TabularInline agar bisa menambah Lesson langsung dari halaman Course
class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category')
    list_filter = ('category', 'instructor')
    search_fields = ('title',)
    inlines = [LessonInline]

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at')
    list_filter = ('course', 'enrolled_at')
    search_fields = ('student__username', 'course__title')

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('get_student', 'lesson', 'is_completed')
    list_filter = ('is_completed',)

    def get_student(self, obj):
        return obj.enrollment.student.username
    get_student.short_description = 'Student'
# Register your models here.
