# student_app/permissions.py
from django.contrib.auth.models import AbstractUser
from rest_framework import permissions
from rest_framework import request
class IsAdminOrReadOnly(permissions.BasePermission):
  """
  Custom permission to only allow admin users to edit objects.
  """




  def has_permission(self, request, view):
      if request.method in permissions.SAFE_METHODS:
          return True
      return request.user and request.user.is_staff







