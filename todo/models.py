from django.db import models

# Create your models here.
class Task(models.Model):
    priority_choices = [
        (0, 'High'),
        (1, 'Normal'),
        (2, 'Low'),
    ]
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.IntegerField(default=1, choices=priority_choices)
    deadline = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    def __str__(self):
        return self.title