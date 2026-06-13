from django.db import models
from django.contrib.auth.models import User


class DailyGoal(models.Model):
    DAILY = 'DAILY'
    WEEKDAYS = 'WEEKDAYS'

    GOAL_TYPE_CHOICES = [
        (DAILY, 'Daily'),
        (WEEKDAYS, 'Weekdays'),    
        ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    goal_type = models.CharField(max_length=10, choices=GOAL_TYPE_CHOICES, default=DAILY)
    current_streak = models.PositiveIntegerField(default=0)
    best_streak = models.PositiveIntegerField(default=0)
    last_completed = models.DateField(null=True, blank=True)
    is_paused = models.BooleanField(default=False)
    paused_at = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title} ({self.get_goal_type_display()})"
    

class GoalLog(models.Model):
    COMPLETED = 'completed'
    SKIPPED = 'skipped'
    STATUS_CHOICES = [
        (COMPLETED, 'Completed'),
        (SKIPPED, 'Skipped'),
    ]
    goal = models.ForeignKey(DailyGoal, on_delete=models.CASCADE, related_name='logs')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('goal', 'date')
    def __str__(self):
        return f"{self.goal.title} - {self.get_status_display()} on {self.date}"
