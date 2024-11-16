from django.urls import path
from .views import CourseListView, CourseDetailView, CourseRegistrationView,ListUserCourseRegistrationsAPIView,CheckRegistration,UserCourseReviewView

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/<int:course_id>/', CourseDetailView.as_view(), name='course-detail'),
    path('register-course/', CourseRegistrationView.as_view(), name='course-register'),
    path('list-register-course/', ListUserCourseRegistrationsAPIView.as_view(), name='list-course-register'),
    path('check-registration/<int:course_id>/', CheckRegistration.as_view(), name='check-course-register'),
    path('course/<int:course_id>/review/', UserCourseReviewView.as_view(), name='user-course-review'),

]
