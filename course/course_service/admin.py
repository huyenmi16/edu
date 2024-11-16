from django.contrib import admin
from .models import Course, Chapter, Lesson, CourseRegistration, CourseReview

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'duration', 'price', 'level')
    search_fields = ('title', 'description', 'instructor')
    list_filter = ('level',)

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    search_fields = ('title', 'course__title')
    list_filter = ('course',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter', 'type', 'duration')
    search_fields = ('title', 'chapter__title', 'type')
    list_filter = ('type', 'chapter')

@admin.register(CourseRegistration)
class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'course', 'registration_date')
    search_fields = ('user_id', 'course__title')
    list_filter = ('registration_date',)

@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'course_id', 'rating', 'review', 'review_date')
    search_fields = ('user_id',)
    list_filter = ('review_date',)
