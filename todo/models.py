from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    PRIORITY_CHOICES = [
        (0, "High"),
        (1, "Normal"),
        (2, "Low"),
    ]

    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.IntegerField(
        default=1,
        choices=PRIORITY_CHOICES
    )
    deadline = models.DateTimeField(
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class TaskHistory(models.Model):
    COMPLETED = "COMPLETED"
    DELETED = "DELETED"
    ACTION_CHOICES = [
        (COMPLETED, "Completed"),
        (DELETED, "Deleted"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.title} - {self.action}"

    class Meta:
        ordering = ["-created_at"]