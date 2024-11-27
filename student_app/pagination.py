from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class StandardResultsSetPagination(PageNumberPagination):
   page_size = 5
   page_size_query_param = 'page_size'
   max_page_size = 100
   page_query_param = 'page'


class StandardLimitOffsetPagination(LimitOffsetPagination):
   default_limit = 5
   limit_query_param = 'limit'
   offset_query_param = 'offset'
   max_limit = 100


class StandardCursorPagination(CursorPagination):
   page_size = 5
   ordering = '-created'
   cursor_query_param = 'cursor'



