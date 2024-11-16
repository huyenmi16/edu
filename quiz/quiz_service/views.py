import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Question, Quiz, UserQuizCompletion
from .serializers import QuestionSerializer,QuizSerializer,QuizCompletionSerializer
from django.shortcuts import get_object_or_404
from django.utils import timezone

class QuestionCreateView(APIView):
    def post(self, request, format=None):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            # Xác minh khóa học tồn tại
            course_id = serializer.validated_data.get('course')
            course_response = requests.get(f'http://127.0.0.1:8000/api/courses/{course_id}/')
            if course_response.status_code == 200:
                # Lưu câu hỏi nếu khóa học tồn tại
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuizListView(APIView):
    def get(self, request, format=None):
        
        token = request.headers.get('Authorization')

        # Gọi endpoint của dịch vụ ngoài để lấy danh sách khóa học đã đăng ký
        register_course_url = "http://127.0.0.1:8000/api/list-register-course/"
        headers = {'Authorization': token}
        
        try:
            response = requests.get(register_course_url, headers=headers)
            response.raise_for_status()
            registered_course_data = response.json()
        except requests.exceptions.RequestException as e:
            return Response({'error': 'Không thể lấy danh sách khóa học đã đăng ký', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        registered_course_ids = registered_course_data.get('registered_course_ids', [])

        if not registered_course_ids:
            return Response({'error': 'Người dùng chưa đăng ký khóa học nào'}, status=status.HTTP_403_FORBIDDEN)

        # Lấy các câu hỏi từ các khóa học đã đăng ký
        questions = Question.objects.filter(course_id__in=registered_course_ids)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListQuizView(APIView):
    def get(self, request, format=None):
        
        token = request.headers.get('Authorization')

        # Gọi endpoint của dịch vụ ngoài để lấy danh sách khóa học đã đăng ký
        register_course_url = "http://127.0.0.1:8000/api/list-register-course/"
        headers = {'Authorization': token}
        
        try:
            response = requests.get(register_course_url, headers=headers)
            response.raise_for_status()
            registered_course_data = response.json()
        except requests.exceptions.RequestException as e:
            return Response({'error': 'Không thể lấy danh sách khóa học đã đăng ký', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        registered_course_ids = registered_course_data.get('registered_course_ids', [])

        if not registered_course_ids:
            return Response({'error': 'Người dùng chưa đăng ký khóa học nào'}, status=status.HTTP_403_FORBIDDEN)

        # Lấy các câu hỏi từ các khóa học đã đăng ký
        quizs = Quiz.objects.filter(course_id__in=registered_course_ids)
        serializer = QuizSerializer(quizs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DetailQuiz(APIView):
    def get(self, request, quiz_id):
        # Retrieve the specific Quiz instance by ID
        quiz = get_object_or_404(Quiz, id=quiz_id)

        # Retrieve all questions related to this quiz
        questions = quiz.questions.all()

        # Serialize the question data
        serializer = QuestionSerializer(questions, many=True)

        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# class SubmitQuiz(APIView):
#     def post(self, request, quiz_id):
#         # Lấy token từ header
#         token = request.headers.get('Authorization')
#         if not token:
#             return Response({'error': 'Yêu cầu token xác thực'}, status=status.HTTP_401_UNAUTHORIZED)
#
#         # Gọi API để lấy thông tin người dùng từ token
#         profile_url = "http://127.0.0.1:4000/api/profile/"
#         headers = {'Authorization': token}
#
#         try:
#             response = requests.get(profile_url, headers=headers)
#             response.raise_for_status()  # Gây ra lỗi nếu status code không phải 2xx
#         except requests.exceptions.RequestException as e:
#             return Response({'error': 'Xác thực người dùng thất bại', 'details': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
#
#         # Lấy dữ liệu người dùng từ response
#         user_data = response.json()
#         user_id = user_data.get('id')
#
#         if not user_id:
#             return Response({'error': 'Dữ liệu người dùng không hợp lệ'}, status=status.HTTP_401_UNAUTHORIZED)
#
#         # Lấy quiz từ quiz_id
#         try:
#             quiz = Quiz.objects.get(id=quiz_id)
#         except Quiz.DoesNotExist:
#             return Response({'error': 'Quiz không tồn tại'}, status=status.HTTP_404_NOT_FOUND)
#
#         # Kiểm tra xem người dùng đã hoàn thành quiz chưa
#         try:
#             user_quiz_completion = UserQuizCompletion.objects.get(user_id=user_id, quiz_id=quiz)
#         except UserQuizCompletion.DoesNotExist:
#             user_quiz_completion = None
#
#         # Nếu chưa hoàn thành, lưu thông tin hoàn thành
#         if not user_quiz_completion:
#             completion_data = {
#                 'user_id': user_id,
#                 'quiz_id': quiz_id,
#                 'is_completed': True,
#                 'completed_at': timezone.now()
#             }
#             serializer = QuizCompletionSerializer(data=completion_data)
#
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response({'message': 'Quiz đã hoàn thành thành công'}, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         # Nếu đã hoàn thành quiz, trả về thông báo
#         return Response({'message': 'Người dùng đã hoàn thành quiz này trước đó'}, status=status.HTTP_200_OK)
#
#
# class CheckSubmit(APIView):
#
#     def get(self, request,quiz_id):
#         # Lấy token từ header
#         token = request.headers.get('Authorization')
#         if not token:
#             return Response({'error': 'Yêu cầu token xác thực'}, status=status.HTTP_401_UNAUTHORIZED)
#
#         profile_url = "http://127.0.0.1:4000/api/profile/"
#         headers = {'Authorization': token}
#
#         try:
#             response = requests.get(profile_url, headers=headers)
#             response.raise_for_status()  # Gây ra lỗi nếu status code không tốt
#         except requests.exceptions.RequestException as e:
#             return Response({'error': 'Xác thực người dùng thất bại', 'details': str(e)},
#                             status=status.HTTP_401_UNAUTHORIZED)
#
#         # Lấy dữ liệu người dùng từ response
#         user_data = response.json()
#         user_id = user_data.get('id')
#
#         if not user_id:
#             return Response({'error': 'Dữ liệu người dùng không hợp lệ'}, status=status.HTTP_401_UNAUTHORIZED)
#
#         # is_registered = CourseRegistration.objects.filter(user_id=user_id,course_id=course_id)
#
#         try:
#             # Kiểm tra xem người dùng đã đăng ký khóa học chưa
#             is_completed = UserQuizCompletion.objects.filter(user_id=user_id, quiz_id=quiz_id).exists()
#             return Response({"is_completed": is_completed})
#         except UserQuizCompletion.DoesNotExist:
#             return Response({"detail": "Course not found"}, status=404)
#


class SubmitQuiz(APIView):
    def post(self, request, quiz_id):
        # Lấy token từ header
        token = request.headers.get('Authorization')
        if not token:
            return Response({'error': 'Yêu cầu token xác thực'}, status=status.HTTP_401_UNAUTHORIZED)

        # Gọi API để lấy thông tin người dùng từ token
        profile_url = "http://127.0.0.1:4000/api/profile/"
        headers = {'Authorization': token}

        try:
            response = requests.get(profile_url, headers=headers)
            response.raise_for_status()  # Gây ra lỗi nếu status code không phải 2xx
        except requests.exceptions.RequestException as e:
            return Response({'error': 'Xác thực người dùng thất bại', 'details': str(e)},
                            status=status.HTTP_401_UNAUTHORIZED)

        # Lấy dữ liệu người dùng từ response
        user_data = response.json()
        user_id = user_data.get('id')

        if not user_id:
            return Response({'error': 'Dữ liệu người dùng không hợp lệ'}, status=status.HTTP_401_UNAUTHORIZED)

        # Lấy quiz từ quiz_id
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({'error': 'Quiz không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        # Kiểm tra xem người dùng đã hoàn thành quiz chưa
        user_quiz_completion, created = UserQuizCompletion.objects.get_or_create(
            user_id=user_id,
            quiz_id=quiz,
            defaults={
                'is_completed': True,
                'completed_at': timezone.now()
            }
        )

        if created:
            # Nếu người dùng chưa hoàn thành, lưu thông tin hoàn thành
            return Response({'message': 'Quiz đã hoàn thành thành công'}, status=status.HTTP_201_CREATED)
        else:
            # Nếu người dùng đã hoàn thành trước đó
            return Response({'message': 'Người dùng đã hoàn thành quiz này trước đó'}, status=status.HTTP_200_OK)


class CheckSubmit(APIView):

    def get(self, request, quiz_id):
        # Lấy token từ header
        token = request.headers.get('Authorization')
        if not token:
            return Response({'error': 'Yêu cầu token xác thực'}, status=status.HTTP_401_UNAUTHORIZED)

        # Gọi API để lấy thông tin người dùng từ token
        profile_url = "http://127.0.0.1:4000/api/profile/"
        headers = {'Authorization': token}

        try:
            response = requests.get(profile_url, headers=headers)
            response.raise_for_status()  # Gây ra lỗi nếu status code không phải 2xx
        except requests.exceptions.RequestException as e:
            return Response({'error': 'Xác thực người dùng thất bại', 'details': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        # Lấy dữ liệu người dùng từ response
        user_data = response.json()
        user_id = user_data.get('id')

        if not user_id:
            return Response({'error': 'Dữ liệu người dùng không hợp lệ'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Kiểm tra xem người dùng đã hoàn thành quiz chưa
            is_completed = UserQuizCompletion.objects.filter(user_id=user_id, quiz_id=quiz_id).exists()

            return Response({"is_completed": is_completed}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Đã xảy ra lỗi khi kiểm tra quiz", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
