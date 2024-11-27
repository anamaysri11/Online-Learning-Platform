from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PersonViewSet, ProfileViewSet, InstructorViewSet, StudentViewSet, CourseViewSet, ModuleViewSet, EnrollmentViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'persons', PersonViewSet, basename='person')
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'instructors', InstructorViewSet, basename='instructor')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'modules', ModuleViewSet, basename='module')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
router.register(r'reviews', ReviewViewSet, basename='review')


urlpatterns = [
  path('api/', include(router.urls)),
  path('api/auth/', include('dj_rest_auth.urls')),
  path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
]







