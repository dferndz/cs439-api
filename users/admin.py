from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from django.contrib import messages

from .models import User
from .forms import RegisterStudentForm


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'csid', 'eid', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("register-student/", self.register_student_view, name="register_student")
        ]
        return my_urls + urls

    def register_student_view(self, request):
        if request.method == "POST":
            eid = request.POST.get("eid")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")

            if eid and first_name and last_name:
                if User.objects.filter(eid=eid).exists():
                    messages.error(request, "Student already registered")
                else:
                    User.objects.create(eid=eid, first_name=first_name, last_name=last_name)
                    messages.success(request, "Student registered")

        context = dict(
            self.admin_site.each_context(request),
            register_student_form=RegisterStudentForm()
        )
        return TemplateResponse(request, "users/register-student.html", context)
