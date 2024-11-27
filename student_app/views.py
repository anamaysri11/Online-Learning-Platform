from django.utils.decorators import method_decorator
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import F, Q, Value, Case, When, Count
from .models import Person, Profile, Instructor, Student, Course, Module, Enrollment, Review, StudentCourse
from .serializers import PersonSerializer, ProfileSerializer, InstructorSerializer, StudentSerializer, CourseSerializer, ModuleSerializer, EnrollmentSerializer, ReviewSerializer
from .pagination import StandardResultsSetPagination
from django.views.decorators.cache import cache_page
from .decorators import handle_exceptions  # Import the decorator
from django.db.models import Avg, Min, Max, Sum, Count
from django.db import transaction
from django.db.transaction import on_commit
from datetime import timedelta
from django.db import models
from django.db.models.functions import Concat
from django.db.models import F, Value


CACHE_TTL = 60 * 15  # 15 minutes.


class PersonViewSet(viewsets.ModelViewSet):
   # Rest of the code...
   serializer_class = PersonSerializer
   pagination_class = StandardResultsSetPagination


   def get_queryset(self):
       return Person.objects.select_related('profile').annotate(
           full_name=Concat(F('first_name'), Value(' '), F('last_name'))
       ).order_by('last_name')[:10]


   @method_decorator(cache_page(CACHE_TTL))
   @handle_exceptions
   def list(self, request, *args, **kwargs):
       queryset = self.get_queryset()
       serializer = self.get_serializer(queryset, many=True)
       return Response(serializer.data)


   @handle_exceptions
   @transaction.atomic
   def create(self, request, *args, **kwargs):
       person, created = Person.objects.get_or_create(
           email=request.data['email'],
           defaults={
               'first_name': request.data['first_name'],
               'last_name': request.data['last_name'],
               'phone_number': request.data['phone_number'],
               'address': request.data['address'],
               'password': request.data['password']
           }
       )
       if not created:
           return Response({'error': 'Person with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
       person.full_clean()  # Ensuring the data is valid
       person.save()


       def post_commit():
           # Post-commit actions
           pass


       on_commit(post_commit)


       serializer = self.get_serializer(person)
       return Response(serializer.data, status=status.HTTP_201_CREATED)


   @handle_exceptions
   def retrieve(self, request, *args, **kwargs):
       instance = self.get_object()
       instance.full_clean()  # Ensuring the data is valid before saving
       instance.save()  # Using save() to persist changes
       return super().retrieve(request, *args, **kwargs)




@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ProfileViewSet(viewsets.ModelViewSet):
   serializer_class = ProfileSerializer
   pagination_class = StandardResultsSetPagination


   def get_queryset(self):
       return Profile.objects.select_related('person').order_by('-person__last_name')[:10]


   @handle_exceptions
   def list(self, request, *args, **kwargs):
       queryset = self.get_queryset()
       serializer = self.get_serializer(queryset, many=True)
       return Response(serializer.data)


   @handle_exceptions
   @transaction.atomic
   def create(self, request, *args, **kwargs):
       profile, created = Profile.objects.get_or_create(
           person_id=request.data['person'],
           defaults={'bio': request.data['bio']}
       )
       if not created:
           return Response({'error': 'Profile for this person already exists'}, status=status.HTTP_400_BAD_REQUEST)
       profile.full_clean()  # Ensuring the data is valid
       profile.save()


       def post_commit():
           # Post-commit actions
           pass


       on_commit(post_commit)


       serializer = self.get_serializer(profile)
       return Response(serializer.data, status=status.HTTP_201_CREATED)




class InstructorViewSet(viewsets.ModelViewSet):
   serializer_class = InstructorSerializer
   pagination_class = StandardResultsSetPagination


   def get_queryset(self):
       return Instructor.objects.select_related('person').filter(salary__gte=50000).exclude(bio='Retired').order_by('-salary')[:10]


   @method_decorator(cache_page(CACHE_TTL))
   @handle_exceptions
   def list(self, request, *args, **kwargs):
       queryset = self.get_queryset()
       serializer = self.get_serializer(queryset, many=True)
       return Response(serializer.data)


   @handle_exceptions
   @transaction.atomic
   def create(self, request, *args, **kwargs):
       instructor, created = Instructor.objects.get_or_create(
           person_id=request.data['person'],
           defaults={'bio': request.data['bio'], 'salary': request.data['salary']}
       )
       if not created:
           return Response({'error': 'Instructor for this person already exists'}, status=status.HTTP_400_BAD_REQUEST)
       instructor.full_clean()  # Ensuring the data is valid
       instructor.save()


       def post_commit():
           # Post-commit actions
           pass


       on_commit(post_commit)


       serializer = self.get_serializer(instructor)
       return Response(serializer.data, status=status.HTTP_201_CREATED)


   @handle_exceptions
   def retrieve(self, request, *args, **kwargs):
       instance = self.get_object()
       instance.full_clean()  # Ensuring the data is valid before saving
       instance.save()  # Using save() to persist changes
       return super().retrieve(request, *args, **kwargs)


   @handle_exceptions
   def get_high_salary_instructors(self, request, *args, **kwargs):
       high_salary_instructors = Instructor.objects.filter(salary__gte=F('salary') * 1.2)
       serializer = self.get_serializer(high_salary_instructors, many=True)
       return Response(serializer.data)




@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class StudentViewSet(viewsets.ModelViewSet):
   serializer_class = StudentSerializer
   pagination_class = StandardResultsSetPagination


   def get_queryset(self):
       return Student.objects.select_related('person').prefetch_related('courses').filter(courses__name='Mathematics').exclude(registration_number__startswith='2022').order_by('registration_number')[:10]


   @handle_exceptions
   def list(self, request, *args, **kwargs):
       queryset = self.get_queryset()
       serializer = self.get_serializer(queryset, many=True)
       return Response(serializer.data)


   @handle_exceptions
   @transaction.atomic
   def create(self, request, *args, **kwargs):
       student, created = Student.objects.get_or_create(
           person_id=request.data['person'],
           defaults={'registration_number': request.data['registration_number']}
       )
       if not created:
           return Response({'error': 'Student for this person already exists'}, status=status.HTTP_400_BAD_REQUEST)
       student.full_clean()  # Ensuring the data is valid
       student.save()


       def post_commit():
           # Post-commit actions
           pass


       on_commit(post_commit)


       serializer = self.get_serializer(student)
       return Response(serializer.data, status=status.HTTP_201_CREATED)


   @handle_exceptions
   def retrieve(self, request, *args, **kwargs):
       instance = self.get_object()
       instance.full_clean()  # Ensuring the data is valid before saving
       instance.save()  # Using save() to persist changes
       return super().retrieve(request, *args, **kwargs)


   @handle_exceptions
   def update_courses(self, request, *args, **kwargs):
       student = self.get_object()
       courses_data = request.data.get('courses', [])
       student.courses.set(courses_data)
       student.save()
       return Response({'status': 'courses updated'}, status=status.HTTP_200_OK)


   @handle_exceptions
   def get_student_marks(self, request, *args, **kwargs):
       student = self.get_object()
       marks = student.studentcourse_set.aggregate(Avg('marks'), Min('marks'), Max('marks'), Sum('marks'))
       return Response(marks, status=status.HTTP_200_OK)


   @handle_exceptions
   def get_high_achievers(self, request, *args, **kwargs):
       high_achievers = Student.objects.filter(studentcourse__marks__gte=90).distinct()
       serializer = self.get_serializer(high_achievers, many=True)
       return Response(serializer.data, status=status.HTTP_200_OK)


   @handle_exceptions
   def get_recent_students(self, request, *args, **kwargs):
       recent_students = Student.objects.filter(person__date_joined__gte=F('person__date_joined') - timedelta(days=30))
       serializer = self.get_serializer(recent_students, many=True)
       return Response(serializer.data, status=status.HTTP_200_OK)


   @handle_exceptions
   def get_top_students(self, request, *args, **kwargs):
       students = Student.objects.annotate(
           high_achiever=Case(
               When(studentcourse__marks__gte=85, then=Value(True)),
               default=Value(False),
               output_field=models.BooleanField(),
           )
       ).filter(high_achiever=True)
       serializer = self.get_serializer(students, many=True)
       return Response(serializer.data)




@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class CourseViewSet(viewsets.ModelViewSet):
   serializer_class = CourseSerializer
   pagination_class = StandardResultsSetPagination


   def get_queryset(self):
       return Course.objects.select_related('instructor').prefetch_related('students', 'reviews').filter(instructor__salary__gte=50000).exclude(description='Deprecated Course').order_by('name')[:10]


   @handle_exceptions
   def list(self, request, *args, **kwargs):
       queryset = self.get_queryset()
       serializer = self.get_serializer(queryset, many=True)
       return Response(serializer.data)


   @handle_exceptions
   @transaction.atomic
   def create(self, request, *args, **kwargs):
       course, created = Course.objects.get_or_create(
           name=request.data['name'],
           defaults={'description': request.data['description'], 'instructor_id': request.data['instructor']}
       )
       if not created:
           return Response({'error': 'Course with this name already exists'}, status=status.HTTP_400_BAD_REQUEST)
       course.full_clean()  # Ensuring the data is valid
       course.save()


       def post_commit():
           # Post-commit actions
           pass


       on_commit(post_commit)


       serializer = self.get_serializer(course)
       return Response(serializer.data, status=status.HTTP_201_CREATED)


   @handle_exceptions
   def retrieve(self, request, *args, **kwargs):
       instance = self.get_object()
       enrollments_count = instance.enrollments.count()  # Using count() to get number of enrollments
       latest_enrollment = instance.enrollments.latest('enrollment_date')  # Using latest() to get the latest enrollment
       instance.full_clean()  # Ensuring the data is valid before saving
       instance.save()
       return super().retrieve(request, *args, **kwargs)


   @handle_exceptions
   def update_students(self, request, *args, **kwargs):
       course = self.get_object()
       students_data = request.data.get('students', [])
       course.students.set(students_data)
       course.save()
       return Response({'status': 'students updated'}, status=status.HTTP_200_OK)


   @handle_exceptions
   def get_course_statistics(self, request, *args, **kwargs):
       course = self.get_object()
       statistics = course.reviews.aggregate(Avg('rating'), Min('rating'), Max('rating'), Sum('rating'))
       return Response(statistics, status=status.HTTP_200_OK)


   @handle_exceptions
   def get_top_students(self, request, *args, **kwargs):
       course = self.get_object()
       top_students = course.students.filter(studentcourse__marks__gte=85).order_by('-studentcourse__marks')
       serializer = self.get_serializer(top_students, many=True)
       return Response(serializer.data, status=status.HTTP_200_OK)


   @handle_exceptions
   def get_recent_courses(self, request, *args, **kwargs):
       recent_courses = Course.objects.filter(created_at__gte=F('created_at') - timedelta(days=30))
       serializer = self.get_serializer(recent_courses, many=True)
       return Response(serializer.data, status=status.HTTP_200_OK)




@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ModuleViewSet(viewsets.ModelViewSet):
   serializer_class = ModuleSerializer
   pagination_class = StandardResultsSetPagination


   def get_queryset(self):
       return Module.objects.select_related('course').filter(course__name='Mathematics').order_by('-name')[:10]


   @handle_exceptions
   def list(self, request, *args, **kwargs):
       queryset = self.get_queryset()
       serializer = self.get_serializer(queryset, many=True)
       return Response(serializer.data)


   @handle_exceptions
   @transaction.atomic
   def create(self, request, *args, **kwargs):
       module, created = Module.objects.get_or_create(
           name=request.data['name'],
           defaults={'description': request.data['description'], 'course_id': request.data['course']}
       )
       if not created:
           return Response({'error': 'Module with this name already exists'}, status=status.HTTP_400_BAD_REQUEST)
       module.full_clean()  # Ensuring the data is valid
       module.save()


       def post_commit():
           # Post-commit actions
           pass


       on_commit(post_commit)


       serializer = self.get_serializer(module)
       return Response(serializer.data, status=status.HTTP_201_CREATED)




@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class EnrollmentViewSet(viewsets.ModelViewSet):
   serializer_class = EnrollmentSerializer
   pagination_class = StandardResultsSetPagination


   def get_queryset(self):
       return Enrollment.objects.select_related('student', 'course').filter(course__name='Mathematics').order_by('-enrollment_date')[:5]


   @handle_exceptions
   def list(self, request, *args, **kwargs):
       queryset = self.get_queryset()
       serializer = self.get_serializer(queryset, many=True)
       return Response(serializer.data)


   @handle_exceptions
   @transaction.atomic
   def create(self, request, *args, **kwargs):
       enrollment, created = Enrollment.objects.get_or_create(
           student_id=request.data['student'],
           course_id=request.data['course']
       )
       if not created:
           return Response({'error': 'This enrollment already exists'}, status=status.HTTP_400_BAD_REQUEST)
       enrollment.full_clean()  # Ensuring the data is valid
       enrollment.save()


       def post_commit():
           # Post-commit actions
           pass


       on_commit(post_commit)


       serializer = self.get_serializer(enrollment)
       return Response(serializer.data, status=status.HTTP_201_CREATED)


   @handle_exceptions
   def retrieve(self, request, *args, **kwargs):
       instance = self.get_object()
       instance.full_clean()  # Ensuring the data is valid before saving
       instance.save()  # Using save() to persist changes
       return super().retrieve(request, *args, **kwargs)


   @handle_exceptions
   def get_recent_enrollments(self, request, *args, **kwargs):
       recent_enrollments = Enrollment.objects.filter(enrollment_date__gte=F('enrollment_date') - timedelta(days=30))
       serializer = self.get_serializer(recent_enrollments, many=True)
       return Response(serializer.data, status=status.HTTP_200_OK)




@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ReviewViewSet(viewsets.ModelViewSet):
   serializer_class = ReviewSerializer
   pagination_class = StandardResultsSetPagination


   def get_queryset(self):
       return Review.objects.select_related('course', 'student').filter(rating__gte=4).exclude(comment__isnull=True).order_by('-rating')[:10]


   @handle_exceptions
   def list(self, request, *args, **kwargs):
       queryset = self.get_queryset()
       serializer = self.get_serializer(queryset, many=True)
       return Response(serializer.data)


   @handle_exceptions
   @transaction.atomic
   def create(self, request, *args, **kwargs):
       review, created = Review.objects.get_or_create(
           student_id=request.data['student'],
           course_id=request.data['course'],
           defaults={'rating': request.data['rating'], 'comment': request.data['comment']}
       )
       if not created:
           return Response({'error': 'This review already exists'}, status=status.HTTP_400_BAD_REQUEST)
       review.full_clean()  # Ensuring the data is valid
       review.save()


       def post_commit():
           # Post-commit actions
           pass


       on_commit(post_commit)


       serializer = self.get_serializer(review)
       return Response(serializer.data, status=status.HTTP_201_CREATED)


   @handle_exceptions
   def retrieve(self, request, *args, **kwargs):
       instance = self.get_object()
       instance.full_clean()  # Ensuring the data is valid before saving
       instance.save()  # Using save() to persist changes
       return super().retrieve(request, *args, **kwargs)


   @handle_exceptions
   def get_review_statistics(self, request, *args, **kwargs):
       reviews = Review.objects.all()
       statistics = reviews.aggregate(Avg('rating'), Min('rating'), Max('rating'), Sum('rating'))
       return Response(statistics, status=status.HTTP_200_OK)


   @handle_exceptions
   def get_recent_reviews(self, request, *args, **kwargs):
       recent_reviews = Review.objects.filter(created_at__gte=F('created_at') - timedelta(days=30))
       serializer = self.get_serializer(recent_reviews, many=True)
       return Response(serializer.data, status=status.HTTP_200_OK)



