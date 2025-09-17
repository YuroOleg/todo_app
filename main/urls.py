from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('add/', views.task_adding, name="add"),
    path('done/', views.tasks_done, name="done"),
    path('failed/', views.tasks_failed, name="failed"),
    path('edit/<int:id>/', views.task_editing, name="edit"),
    path('delete/<int:id>/', views.task_deleting, name="delete"),
]