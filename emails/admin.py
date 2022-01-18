from django.conf.urls import url
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from django.contrib import messages

# from emails.models import Email
#
# For security reasons this functionality is disabled
# @admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ['recipients', 'sent', 'sent_on', 'send_button']
    list_filter = ['sent', 'sent_on']
    search_fields = ['recipients']

    actions = ['send_email']

    @admin.action(description="Send selected email")
    def send_email(self, request, queryset):
        for email in queryset:
            email.send()

    def send_button(self, obj):
        if obj.sent:
            title = "Resend"
        else:
            title = "Send"

        url = reverse('admin:send-single-email', args=[obj.pk])

        return format_html(
            f"<a class='button' href='{url}'>{title}</a>&nbsp;",
        )
    send_button.short_description = 'Actions'
    send_button.allow_tags = True

    def send_single_email(self, request, email_id):
        email = self.get_object(request, email_id)
        if email.send():
            messages.add_message(request, messages.SUCCESS, message="Email sent.")
        else:
            messages.add_message(request, messages.WARNING, message="Could not send email")

        return redirect("admin:emails_email_changelist")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<email_id>.+)/send/$',
                self.admin_site.admin_view(self.send_single_email),
                name='send-single-email',
            ),
        ]
        return custom_urls + urls
