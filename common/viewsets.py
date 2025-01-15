from rest_framework import status
from rest_framework.response import Response


class MappingViewSetMixin(object):
    serializer_action_classes = {}

    def get_serializer_class(self):
        if self.serializer_action_classes.get(self.action, None):
            return self.serializer_action_classes[self.action]
        return self.serializer_class

    def handle_paginated_response(self, queryset):
        page_queryset = self.paginate_queryset(queryset)
        if page_queryset is not None:
            serializer = self.get_serializer(page_queryset, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
