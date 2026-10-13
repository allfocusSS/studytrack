from django.conf import settings
from django.db import models
from django.utils import timezone


class Assignment(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assignments")
    title = models.CharField(max_length=160)
    subject = models.CharField(max_length=100)
    description = models.TextField(max_length=5000, blank=True)
    deadline = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_overdue(self):
        return not self.is_completed and self.deadline is not None and self.deadline < timezone.localdate()

    def __str__(self):
        return self.title
