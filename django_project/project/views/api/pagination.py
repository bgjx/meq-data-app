from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

class DataTablesPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'length'
    page_query_param = 'page'

    def paginate_queryset(self, queryset, request, view= None):
        self.draw = int(request.GET.get('draw', 1))
        try:
            self.length = int(request.GET.get('length', self.page_size))
        except (ValueError, TypeError):
            self.length = self.page_size
        
        try:
            self.start = int(request.GET.get('start', 0))
        except(ValueError, TypeError):
            self.start = 0

        self.request = request

        if not queryset.exists():
            self.page = None
            return []

        page_number = (self.start // self.length) + 1
        if page_number < 1:
            page_number = 1

        request.query_params._mutable = True 
        request.query_params['page'] = page_number
        request.query_params._mutable = False

        try:
            paginated_queryset = super().paginate_queryset(queryset, request, view)
            logger.info(f"Paginated {len(paginated_queryset)} items for page {page_number}")
            return paginated_queryset
        except Exception as e:
            logger.error(f"Invalid page error: {str(e)}")
            self.page = None
            return []
    
    def get_paginated_response(self, data):
        return Response(
            {
                'draw': self.draw,
                'recordsTotal': self.page.paginator.count if self.page else 0,
                'recordsFiltered': self.page.paginator.count if self.page else 0,
                'data': data
            }
        )