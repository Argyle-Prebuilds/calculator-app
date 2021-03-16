from rest_framework.utils.urls import replace_query_param, remove_query_param


class ArgyleApiPagination:
    """
    Custom class for handling pagination data fetched from Argyle API.
    """

    def __init__(self, count: int, limit: int, offset: int, request):
        """
        @param count: int
        @param limit: int
        @param offset: int
        @param request: Request
        """
        self.count = count
        self.limit = limit
        self.offset = offset
        self.request = request

        self.limit_query_param = 'limit'
        self.offset_query_param = 'offset'

    def __get_next_link(self):
        if self.offset + self.limit >= self.count:
            return None

        url = self.request.build_absolute_uri()
        url = replace_query_param(url, self.limit_query_param, self.limit)

        offset = self.offset + self.limit
        return replace_query_param(url, self.offset_query_param, offset)

    def __get_previous_link(self):
        if self.offset <= 0:
            return None

        url = self.request.build_absolute_uri()
        url = replace_query_param(url, self.limit_query_param, self.limit)

        if self.offset - self.limit <= 0:
            return remove_query_param(url, self.offset_query_param)

        offset = self.offset - self.limit
        return replace_query_param(url, self.offset_query_param, offset)

    def get_paginated_response(self, data=None):
        if data is None:
            data = []

        return {
            'count': self.count,
            'next': self.__get_next_link(),
            'previous': self.__get_previous_link(),
            'results': data
        }
