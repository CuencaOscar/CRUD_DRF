from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import filters, permissions, viewsets

from apps.crud_app.models import Event
from apps.crud_app.serializer import EventSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List events",
        auth=[],
        parameters=[
            OpenApiParameter("state", description="Two-letter state code, e.g. `TX`"),
            OpenApiParameter("category", description="Exact category, case-insensitive"),
        ],
    ),
    retrieve=extend_schema(summary="Event detail", auth=[]),
    create=extend_schema(summary="Create an event (JWT)"),
    update=extend_schema(summary="Replace an event (JWT)"),
    partial_update=extend_schema(summary="Update some fields of an event (JWT)"),
    destroy=extend_schema(summary="Delete an event (JWT)"),
)
class EventViewSet(viewsets.ModelViewSet):
    """Anyone can browse events; creating, editing and deleting require a JWT access token."""

    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "place", "city", "category"]
    ordering_fields = ["start_date", "title", "city", "created_at"]

    def get_queryset(self):
        queryset = Event.objects.all()
        for field in ("state", "category"):
            value = self.request.query_params.get(field)
            if value:
                queryset = queryset.filter(**{f"{field}__iexact": value})
        return queryset
