from django.contrib import admin
from .models import Resource


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    readonly_fields = ["id"]
    list_display = ["title", "description"]
    search_fields = ["title", "description"]
