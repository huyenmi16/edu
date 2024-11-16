from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Course, CourseRegistration,CourseReview
from .serializers import CourseSerializer
from rest_framework import status
from .serializers import CourseRegistrationSerializer,CourseReviewSerializer
import requests
from rest_framework.exceptions import AuthenticationFailed

class CourseListView(APIView):
    def get(self, request, format=None):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

class CourseDetailView(APIView):
    def get(self, request, course_id, format=None):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Khóa học không tồn tại'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    

class CourseRegistrationView(APIView):
    def post(self, request, format=None):
        # Lấy token từ headers
        token = request.headers.get('Authorization')
        if not token:
            return Response({'error': 'Yêu cầu token xác thực'}, status=status.HTTP_401_UNAUTHORIZED)

        # Gọi dịch vụ người dùng để lấy dữ liệu profile
        profile_url = "http://127.0.0.1:4000/api/profile/"
        headers = {'Authorization': token}
        
        try:
            response = requests.get(profile_url, headers=headers)
            response.raise_for_status()  # Gây ra lỗi nếu status code không tốt
        except requests.exceptions.RequestException as e:
            return Response({'error': 'Xác thực người dùng thất bại', 'details': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        # Lấy dữ liệu người dùng từ response
        user_data = response.json()
        user_id = user_data.get('id')
        
        if not user_id:
            return Response({'error': 'Dữ liệu profile người dùng không hợp lệ'}, status=status.HTTP_401_UNAUTHORIZED)

        # Kiểm tra xem người dùng đã đăng ký khóa học chưa
        course_id = request.data.get('course')
        if CourseRegistration.objects.filter(user_id=user_id, course_id=course_id).exists():
            return Response({'error': 'Người dùng đã đăng ký khóa học này'}, status=status.HTTP_400_BAD_REQUEST)

        # Khi đã có user_id và người dùng chưa đăng ký khóa học, tạo bản ghi đăng ký
        serializer = CourseRegistrationSerializer(data={'user_id': user_id, 'course': course_id,'is_registed':True})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ListUserCourseRegistrationsAPIView(APIView):

    def get(self, request):
        # Lấy token từ header
        token = request.headers.get('Authorization')
        if not token:
            return Response({'error': 'Yêu cầu token xác thực'}, status=status.HTTP_401_UNAUTHORIZED)

        
        profile_url = "http://127.0.0.1:4000/api/profile/"
        headers = {'Authorization': token}
        
        try:
            response = requests.get(profile_url, headers=headers)
            response.raise_for_status()  # Gây ra lỗi nếu status code không tốt
        except requests.exceptions.RequestException as e:
            return Response({'error': 'Xác thực người dùng thất bại', 'details': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        # Lấy dữ liệu người dùng từ response
        user_data = response.json()
        user_id = user_data.get('id')
        
        if not user_id:
            return Response({'error': 'Dữ liệu người dùng không hợp lệ'}, status=status.HTTP_401_UNAUTHORIZED)


        # Truy vấn tất cả các CourseRegistration có user_id tương ứng
        course_registrations = CourseRegistration.objects.filter(user_id=user_id)
        
        # Lấy danh sách các id của course đã đăng ký
        course_ids = course_registrations.values_list('course_id', flat=True)

        # Trả về danh sách id của các khóa học dưới dạng JSON
        return Response({'registered_course_ids': list(course_ids)})
    

class CheckRegistration(APIView):

    def get(self, request,course_id):
        # Lấy token từ header
        token = request.headers.get('Authorization')
        if not token:
            return Response({'error': 'Yêu cầu token xác thực'}, status=status.HTTP_401_UNAUTHORIZED)

        
        profile_url = "http://127.0.0.1:4000/api/profile/"
        headers = {'Authorization': token}
        
        try:
            response = requests.get(profile_url, headers=headers)
            response.raise_for_status()  # Gây ra lỗi nếu status code không tốt
        except requests.exceptions.RequestException as e:
            return Response({'error': 'Xác thực người dùng thất bại', 'details': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        # Lấy dữ liệu người dùng từ response
        user_data = response.json()
        user_id = user_data.get('id')
        
        if not user_id:
            return Response({'error': 'Dữ liệu người dùng không hợp lệ'}, status=status.HTTP_401_UNAUTHORIZED)


        
        # is_registered = CourseRegistration.objects.filter(user_id=user_id,course_id=course_id)

        try:
        # Kiểm tra xem người dùng đã đăng ký khóa học chưa
            is_registered = CourseRegistration.objects.filter(user_id=user_id, course_id=course_id).exists()
            return Response({"is_registered": is_registered})
        except CourseRegistration.DoesNotExist:
            return Response({"detail": "Course not found"}, status=404)
        


class UserCourseReviewView(APIView):
    def post(self, request, course_id, format=None):
        # Lấy token từ headers
        token = request.headers.get('Authorization')
        if not token:
            return Response({'error': 'Yêu cầu token xác thực'}, status=status.HTTP_401_UNAUTHORIZED)

        # Gọi dịch vụ người dùng để lấy dữ liệu profile
        profile_url = "http://127.0.0.1:4000/api/profile/"
        headers = {'Authorization': token}
        
        try:
            response = requests.get(profile_url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return Response({'error': 'Xác thực người dùng thất bại', 'details': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        # Lấy dữ liệu người dùng từ response
        user_data = response.json()
        user_id = user_data.get('id')
        
        if not user_id:
            return Response({'error': 'Dữ liệu người dùng không hợp lệ'}, status=status.HTTP_401_UNAUTHORIZED)

        # Kiểm tra xem người dùng đã đăng ký khóa học chưa
        if not CourseRegistration.objects.filter(user_id=user_id, course_id=course_id).exists():
            return Response({'error': 'Người dùng chưa đăng ký khóa học này'}, status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra xem người dùng đã đánh giá khóa học này chưa
        if CourseReview.objects.filter(user_id=user_id, course_id=course_id).exists():
            return Response({'error': 'Người dùng đã đánh giá khóa học này'}, status=status.HTTP_400_BAD_REQUEST)

        # Tạo đánh giá mới
        serializer = CourseReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=user_id, course_id=course_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, course_id, format=None):
        reviews = CourseReview.objects.filter(course_id=course_id)
        serializer = CourseReviewSerializer(reviews, many=True)
        return Response(serializer.data)
        