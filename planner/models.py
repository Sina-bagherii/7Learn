from django.db import models


class DailyPlan(models.Model):
    """A simple record for a given day's focus and notes."""

    date = models.DateField(unique=True)
    main_focus = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self) -> str:
        return f"Plan for {self.date}"


class PlanItem(models.Model):
    """Tasks or commitments tied to a daily plan."""

    PRIORITY_CHOICES = [
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]

    CATEGORY_CHOICES = [
        ("work", "Work"),
        ("personal", "Personal"),
        ("errand", "Errand"),
        ("health", "Health"),
        ("learning", "Learning"),
    ]

    plan = models.ForeignKey(DailyPlan, related_name="items", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES, blank=True)
    priority = models.CharField(max_length=16, choices=PRIORITY_CHOICES, default="medium")
    scheduled_time = models.TimeField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["is_done", "priority", "scheduled_time", "title"]

    def __str__(self) -> str:
        return self.title
