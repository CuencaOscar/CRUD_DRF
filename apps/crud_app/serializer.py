from rest_framework import serializers
from apps.crud_app.models import Crud


class CrudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crud
        fields = '__all__'