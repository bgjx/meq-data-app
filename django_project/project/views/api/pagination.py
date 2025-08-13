from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class DataTablesPagination(PageNumberPagination):
    page_size_query_param = 'length'
    page_query_param = 'start'

    def paginate_queryset(self, queryset, request, view= None):
        self.draw = int(request.GET.get('draw', 1))
        self.length = int(request.GET.get('length', self.page_size))
        self.start = int(request.GET.get('start', 0))
        self.request = request

        page_number = (self.start // self.length) + 1
        request.query_params._mutable = True 
        request.query_params['page'] = page_number
        request.query_params._mutable = False 

        return super().paginate_queryset(queryset, request, view)
    
    def get_paginated_response(self, data):
        return Response(
            {
                'draw': self.draw,
                'recordsTotal': self.page.paginator.count,
                'recordsFiltered': self.page.paginator.count,
                'data': data
            }
        )