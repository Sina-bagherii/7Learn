import datetime

from django.test import TestCase, override_settings
from django.urls import reverse

from .models import DailyPlan, PlanItem


test_databases = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
}


@override_settings(DATABASES=test_databases)
class PlannerModelTests(TestCase):
    def test_daily_plan_string_representation(self):
        plan = DailyPlan.objects.create(date=datetime.date(2025, 1, 1), main_focus="Launch day")
        self.assertEqual(str(plan), "Plan for 2025-01-01")

    def test_plan_item_defaults(self):
        plan = DailyPlan.objects.create(date=datetime.date.today())
        item = PlanItem.objects.create(plan=plan, title="Review goals")
        self.assertEqual(item.priority, "medium")
        self.assertFalse(item.is_done)
        self.assertEqual(str(item), "Review goals")


@override_settings(DATABASES=test_databases)
class PlannerViewTests(TestCase):
    def test_dashboard_creates_plan_and_task(self):
        target_date = datetime.date(2025, 1, 2)
        response = self.client.get(f"{reverse('planner:dashboard')}?date={target_date}")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(DailyPlan.objects.filter(date=target_date).exists())

        response = self.client.post(
            f"{reverse('planner:dashboard')}?date={target_date}",
            {
                "action": "add_task",
                "task-title": "Draft priorities",
                "task-category": "work",
                "task-priority": "high",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        plan = DailyPlan.objects.get(date=target_date)
        self.assertEqual(plan.items.count(), 1)
        self.assertEqual(plan.items.first().priority, "high")

    def test_toggle_and_delete_task(self):
        plan = DailyPlan.objects.create(date=datetime.date.today())
        item = PlanItem.objects.create(plan=plan, title="Check-in")

        toggle_response = self.client.post(reverse("planner:toggle_task", args=[item.pk]))
        self.assertEqual(toggle_response.status_code, 302)
        item.refresh_from_db()
        self.assertTrue(item.is_done)

        delete_response = self.client.post(reverse("planner:delete_task", args=[item.pk]))
        self.assertEqual(delete_response.status_code, 302)
        self.assertFalse(PlanItem.objects.filter(pk=item.pk).exists())
