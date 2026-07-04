this is my views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import DailyGoalForm
from .models import DailyGoal, GoalLog
from django.utils import timezone
from django.views.decorators.http import require_POST


@login_required
def daily_goals(request):

    if request.method == "POST":
        form = DailyGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return('daily_goals')
    else:
        form = DailyGoalForm()
    
    goals = DailyGoal.objects.filter(user=request.user)
    context = {
        "goals": goals,
        "form": form,
        "completed_today": 0,
        "total_goals": goals.count(),
    }

    return render(request, "daily_goals.html", context)


@login_required
@require_POST
def complete_goal(request, pk):
    today = timezone.localdate()

    goal = get_object_or_404(
        DailyGoal,
        pk=pk,
        user=request.user,
    )

    is_weekend = today.weekday() >= 5

    if goal.goal_type == DailyGoal.WEEKDAYS and is_weekend:
        return redirect("daily_goals")

    log, created = GoalLog.objects.get_or_create(
        goal=goal,
        date=today,
        defaults={"status": GoalLog.COMPLETED},
    )

    return redirect("daily_goals")




this is my forms.py

from django import forms
from django.forms import ModelForm, ValidationError
from .models import DailyGoal


class DailyGoalForm(ModelForm):

    class Meta:
        model = DailyGoal
        fields = ['title', 'goal_type']
        labels = {
            'title':     'Goal',
            'goal_type': 'Frequency',    
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Add Daily Goal and hit enter to add',
            }),
            'goal_type': forms.RadioSelect(),   # ○ Daily  ○ Weekday — cleaner than dropdown
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)   # ← grab user before super()
        super().__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if DailyGoal.objects.filter(user=self.user, title__iexact=title).exists():
            raise forms.ValidationError('A goal with this name already exists.')
        return title
