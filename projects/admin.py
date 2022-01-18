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
    list_display = ["project", "user", "get_csid", "get_eid", "commit", "status"]
    list_filter = ["project__name", "status"]
    search_fields = ["user__first_name", "user__last_name", "project__name", "commit"]
    list_editable = ["status"]
    readonly_fields = ["id"]
    fields = ["id", "project", "user", "commit", "status"]

    def get_csid(self, obj):
        return obj.user.csid

    def get_eid(self, obj):
        return obj.user.eid

    get_csid.short_description = "CSID"
    get_csid.admin_order_field = "user__csid"
    get_eid.short_description = "eID"
    get_eid.admin_order_field = "user__eid"
