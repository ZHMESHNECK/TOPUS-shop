from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class Pagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 80

    def get_paginated_response(self, data):
        return Response({
            'list_page': self.get_html_context(),
            'count_page': True if self.page.paginator.num_pages > 1 else False,
            'page_num': self.page.number,
            'results': data
        })
