# C:\Users\Admin\PyCharmMiscProject\core\admin.py

from django.contrib import admin
# Import all your models, including Content now that it's a top-level model
from .models import CustomUser, Course, Enrollment, Lesson, Assignment, Submission, Category, Content

# ContentInline to manage contents directly within the Lesson admin page
class ContentInline(admin.TabularInline):
    model = Content
    extra = 1 # Number of empty forms to display
    fields = ['title', 'content_type', 'text_content', 'file_content', 'url_content', 'order']


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_student', 'is_teacher', 'is_staff')
    list_filter = ('is_student', 'is_teacher', 'is_staff')
    search_fields = ('username', 'email')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'price', 'start_date', 'end_date', 'difficulty', 'status', 'category')
    list_filter = ('difficulty', 'status', 'category', 'teacher')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date', 'completed')
    list_filter = ('completed', 'enrollment_date')
    search_fields = ('student__username', 'course__title')
    raw_id_fields = ('student', 'course')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'video_url')
    list_filter = ('course',)
    search_fields = ('title', 'content')
    inlines = [ContentInline] # Link ContentInline to LessonAdmin

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'due_date', 'max_score')
    list_filter = ('lesson', 'due_date')
    search_fields = ('title', 'description')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submitted_at', 'score', 'completed')
    list_filter = ('score', 'completed', 'submitted_at')
    search_fields = ('student__username', 'assignment__title')
    raw_id_fields = ('assignment', 'student')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

# You can also register Content as a top-level section in the admin if you wish
admin.site.register(Content)