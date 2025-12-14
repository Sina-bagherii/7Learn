# Generated manually for the planner app
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DailyPlan",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField(unique=True)),
                ("main_focus", models.CharField(blank=True, max_length=255)),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["-date"]},
        ),
        migrations.CreateModel(
            name="PlanItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                (
                    "category",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("work", "Work"),
                            ("personal", "Personal"),
                            ("errand", "Errand"),
                            ("health", "Health"),
                            ("learning", "Learning"),
                        ],
                        max_length=32,
                    ),
                ),
                (
                    "priority",
                    models.CharField(
                        choices=[("high", "High"), ("medium", "Medium"), ("low", "Low")],
                        default="medium",
                        max_length=16,
                    ),
                ),
                ("scheduled_time", models.TimeField(blank=True, null=True)),
                ("duration_minutes", models.PositiveIntegerField(blank=True, null=True)),
                ("is_done", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "plan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="planner.dailyplan",
                    ),
                ),
            ],
            options={"ordering": ["is_done", "priority", "scheduled_time", "title"]},
        ),
    ]
