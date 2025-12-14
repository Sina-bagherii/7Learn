from django.urls import path

from . import views

app_name = "planner"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("tasks/<int:pk>/toggle/", views.toggle_task, name="toggle_task"),
    path("tasks/<int:pk>/delete/", views.delete_task, name="delete_task"),
]
