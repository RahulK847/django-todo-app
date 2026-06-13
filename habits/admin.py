from django.contrib import admin
from .models import DailyGoal, GoalLog

# Register your models here.
admin.site.register(DailyGoal)
admin.site.register(GoalLog)

