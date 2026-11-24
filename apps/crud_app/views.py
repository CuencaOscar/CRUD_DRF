from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from apps.crud_app.models import Crud
from apps.crud_app.serializer import CrudSerializer


class CrudViewSet(viewsets.ViewSet):
    """CRUD endpoints for event records."""

    def crudCreate(self, request):
        serializer = CrudSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def crudRead(self, request):
        events = Crud.objects.all()
        serializer = CrudSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def crudUpdate(self, request, pk):
        event = get_object_or_404(Crud, id=pk)
        serializer = CrudSerializer(instance=event, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def crudDelete(self, request, pk):
        event = get_object_or_404(Crud, id=pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
