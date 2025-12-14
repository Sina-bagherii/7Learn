from django import forms

from .models import DailyPlan, PlanItem


class DailyPlanForm(forms.ModelForm):
    class Meta:
        model = DailyPlan
        fields = ["date", "main_focus", "notes"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "main_focus": forms.TextInput(attrs={"placeholder": "What is the most important outcome today?"}),
            "notes": forms.Textarea(attrs={"rows": 3, "placeholder": "Reminders, habits, or gratitude."}),
        }


class PlanItemForm(forms.ModelForm):
    class Meta:
        model = PlanItem
        fields = ["title", "category", "priority", "scheduled_time", "duration_minutes"]
        widgets = {
            "scheduled_time": forms.TimeInput(attrs={"type": "time"}),
            "duration_minutes": forms.NumberInput(attrs={"min": 5, "step": 5, "placeholder": "30"}),
        }
        help_texts = {
            "title": "Break tasks down so they can be completed in 20-90 minutes.",
            "duration_minutes": "Optional estimate; useful for blocking your calendar.",
        }
