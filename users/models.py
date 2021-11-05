from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from emails.models import Email
from emails.utils import send_email
from .managers import CustomUserManager, PasswordTokenManager


class User(AbstractUser):
    username = None
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def send_email(self, subject, message):
        Email.objects.create(subject=subject, message=message, recipients=[self.email])

    def get_password_token(self):
        token, created = PasswordToken.objects.get_or_create(user=self)
        return token

    def new_password(self):
        token = self.get_password_token()

        send_email(
            subject="Welcome to Recipes!",
            template="accounts/emails/action_email.html",
            recipients=[self.email],
            context={
                "title": "Welcome to recipes",
                "message": "To activate your account and create a password use the button below.",
                "button": {
                    "url": f"http://localhost:8000/api/users/{self.pk}/change-password/{token.token}/",
                    "title": "Activate account",
                },
                "user": self,
                "footer_message": "If you did not sign up on Recipes.com, please disregard this email.",
            },
        )

    def reset_password(self):
        token = self.get_password_token()

        send_email(
            subject="Reset password",
            template="accounts/emails/action_email.html",
            recipients=[self.email],
            context={
                "title": "Reset password",
                "message": "Use the button below to reset your password.",
                "button": {
                    "url": f"http://localhost:8000/api/users/{self.pk}/change-password/{token.token}/",
                    "title": "Reset password",
                },
                "user": self,
                "footer_message": "If you did not request a password reset, please disregard this email",
            },
        )


class PasswordToken(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    token = models.UUIDField(default=uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = PasswordTokenManager()
