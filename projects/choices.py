from django.db import models


class RegradeStatus(models.TextChoices):
    PENDING = "Pending"
    INCREASE = "Grade increased"
    NO_CHANGE = "Grade did not change"
