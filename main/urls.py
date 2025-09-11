from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('add/', views.task_adding, name="add"),
    path('edit/<int:id>/', views.task_editing, name="edit"),
    path('delete/<int:id>/', views.task_deleting, name="delete"),
]