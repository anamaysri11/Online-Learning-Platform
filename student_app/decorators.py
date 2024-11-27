from rest_framework.exceptions import ValidationError, NotAuthenticated, PermissionDenied, NotFound
from rest_framework.response import Response
from rest_framework import status

def handle_exceptions(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            return func(self, request, *args, **kwargs)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except NotAuthenticated as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except NotFound as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return wrapper
