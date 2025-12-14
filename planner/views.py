import datetime

from django.db import models

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods, require_POST
from django.urls import reverse

from .forms import DailyPlanForm, PlanItemForm
from .models import DailyPlan, PlanItem


def _resolve_date(request):
    date_param = request.GET.get("date")
    if date_param:
        try:
            return datetime.datetime.strptime(date_param, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid date format. Showing today instead.")
    return timezone.localdate()


@require_http_methods(["GET", "POST"])
def dashboard(request):
    target_date = _resolve_date(request)
    plan, _ = DailyPlan.objects.get_or_create(date=target_date)

    plan_form = DailyPlanForm(request.POST or None, instance=plan, prefix="plan")
    task_form = PlanItemForm(request.POST or None, prefix="task")

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "update_plan" and plan_form.is_valid():
            plan_form.save()
            messages.success(request, "Daily focus saved.")
            return redirect(f"{reverse('planner:dashboard')}?date={plan.date}")
        if action == "add_task" and task_form.is_valid():
            task = task_form.save(commit=False)
            task.plan = plan
            task.save()
            messages.success(request, "New task added to your day.")
            return redirect(f"{reverse('planner:dashboard')}?date={plan.date}")
        messages.error(request, "Please fix the errors below before continuing.")

    tasks = (
        plan.items.annotate(
            priority_weight=models.Case(
                models.When(priority="high", then=models.Value(3)),
                models.When(priority="medium", then=models.Value(2)),
                models.When(priority="low", then=models.Value(1)),
                default=models.Value(0),
                output_field=models.IntegerField(),
            )
        )
        .order_by("is_done", "-priority_weight", "scheduled_time", "title")
    )
    return render(
        request,
        "planner/dashboard.html",
        {
            "plan": plan,
            "tasks": tasks,
            "plan_form": plan_form,
            "task_form": task_form,
            "target_date": target_date,
        },
    )


@require_POST
def toggle_task(request, pk):
    task = get_object_or_404(PlanItem, pk=pk)
    task.is_done = not task.is_done
    task.save(update_fields=["is_done", "updated_at"])
    messages.success(request, "Task updated.")
    return redirect(f"{reverse('planner:dashboard')}?date={task.plan.date}")


@require_POST
def delete_task(request, pk):
    task = get_object_or_404(PlanItem, pk=pk)
    plan_date = task.plan.date
    task.delete()
    messages.success(request, "Task removed from the plan.")
    return redirect(f"{reverse('planner:dashboard')}?date={plan_date}")
