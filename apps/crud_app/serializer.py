import re

from rest_framework import serializers

from apps.crud_app.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id", "title", "place", "city", "state", "zipcode", "category", "notes",
            "start_date", "end_date", "created_at",
        ]
        read_only_fields = ["created_at"]

    def validate_zipcode(self, value):
        if not re.fullmatch(r"\d{5}(-\d{4})?", value):
            raise serializers.ValidationError("Enter a US ZIP code such as 73301 or 73301-1234.")
        return value

    def validate(self, attrs):
        start = attrs.get("start_date", getattr(self.instance, "start_date", None))
        end = attrs.get("end_date", getattr(self.instance, "end_date", None))
        if start and end and end < start:
            raise serializers.ValidationError({"end_date": "The event cannot end before it starts."})
        return attrs
