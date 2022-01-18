from django.db import models
from uuid import uuid4

from users.models import User
from .choices import RegradeStatus
from emails.utils import send_email


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    modified = models.DateTimeField(auto_now=True, blank=False, null=False)

    name = models.CharField(max_length=512)
    description = models.CharField(max_length=512)
    info_site_name = models.CharField(max_length=512)
    active = models.BooleanField(default=False, blank=False, null=False)

    def __str__(self):
        return self.name


class RegradeRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    modified = models.DateTimeField(auto_now=True, blank=False, null=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    commit = models.CharField(max_length=40)
    status = models.CharField(max_length=512, default=RegradeStatus.PENDING, choices=RegradeStatus.choices)
    old_status = models.CharField(max_length=512, default=RegradeStatus.PENDING, choices=RegradeStatus.choices)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.project.name}"

    def notify_user(self):
        message = f"Hi {self.user.first_name},\n\nWe have received a regrade request for:\n\n"
        regrade_info = f"Project: {self.project.name}\nCommit: {self.commit}\n\n"
        footer = f"You will receive an update when we process your regrade.\n"

        self.user.send_email(
            subject=f"Regrade request for project {self.project.name}",
            message=message+regrade_info+footer
        )

    def notify_status_update(self):
        message = f"Hi {self.user.first_name},\n\nThere is a status update for:\n\n"
        regrade_info = f"Project: {self.project.name}\nCommit: {self.commit}\n"
        status = f"Status: {self.status}\n\n"
        increase_footer = f"Monitor Canvas for a grade update.\n"
        no_change_footer = f"Regrade score was not higher than original score.\n"
        pending_footer = "We are still working on your regrade."

        if self.status == RegradeStatus.INCREASE:
            footer = increase_footer
        elif self.status == RegradeStatus.NO_CHANGE:
            footer = no_change_footer
        else:
            footer = pending_footer

        self.user.send_email(
            subject=f"Regrade status update for project {self.project.name}",
            message=message + regrade_info + status + footer
        )
