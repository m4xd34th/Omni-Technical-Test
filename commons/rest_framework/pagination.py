from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class FullPageNumberPagination(PageNumberPagination):
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        next = self.page.next_page_number() if self.has_next() else None
        previous = self.page.previous_page_number() if self.has_previous() else None

        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("next_link", self.get_next_link()),
                    ("previous_link", self.get_previous_link()),
                    ("next", next),
                    ("previous", previous),
                    ("pages", self.page.paginator.num_pages),
                    ("actual", self.page.number),
                    ("results", data),
                ]
            )
        )

    def has_next(self):
        return self.page.has_next()

    def has_previous(self):
        return self.page.has_previous()


class FullPageNumberPagination10(FullPageNumberPagination):
    page_size = 10
