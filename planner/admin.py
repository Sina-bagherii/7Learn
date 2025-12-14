from django.contrib import admin

from .models import DailyPlan, PlanItem


@admin.register(DailyPlan)
class DailyPlanAdmin(admin.ModelAdmin):
    list_display = ("date", "main_focus", "created_at", "updated_at")
    search_fields = ("main_focus", "notes")
    ordering = ("-date",)


@admin.register(PlanItem)
class PlanItemAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "plan",
        "category",
        "priority",
        "scheduled_time",
        "duration_minutes",
        "is_done",
    )
    list_filter = ("category", "priority", "is_done")
    search_fields = ("title", "plan__main_focus")
    ordering = ("-created_at",)
