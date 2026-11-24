from django.contrib import admin

from apps.crud_app.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "city", "state", "category", "start_date", "end_date"]
    list_filter = ["state", "category"]
    search_fields = ["title", "place", "city"]
