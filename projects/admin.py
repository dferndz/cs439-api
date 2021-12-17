from django.contrib import admin

from .models import Project, RegradeRequest


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "active"]
    list_filter = ["active"]
    search_fields = ["name", "site_info_name", "description"]

    readonly_fields = ["id"]


@admin.register(RegradeRequest)
class RegradeRequestAdmin(admin.ModelAdmin):
    list_display = ["project", "user", "commit", "status"]
    list_filter = ["project__name", "status"]
    search_fields = ["user__first_name", "user__last_name", "project__name", "commit"]
    list_editable = ["status"]
