from rest_framework.response import Response
from apps.crud_app.models import Crud
from apps.crud_app.serializer import CrudSerializer

from rest_framework import viewsets
from rest_framework import status

class CrudViewSet(viewsets.ViewSet):

#Funcion para crear nueva data a mi base de datos
    def crudCreate(self, request):
        serializer = CrudSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

#Funcion para obtener todo la data de mi base de datos
    def crudRead(self, request):
        events = Crud.objects.all()
        serializer = CrudSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#Funcion para actualizar informacion mediante un Id de la data
    def crudUpdate(self, request, pk):
        event = Crud.objects.get(id=pk)
        serializer = CrudSerializer(instance=event, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

#Funcion para eliminar una data por id que pasemos como parametro en la URL      
    def crudDelete(self, request, pk):
        event = Crud.objects.get(id=pk)
        event.delete()
        return Response("Deleted")