from django.urls import path
from .views import create_task, edit_task, delete_task, home, tasks_done, tasks_failed, reminder

urlpatterns = [
    path('', home, name='home'),
    path('create_task/', create_task, name='create_task'),
    path('edit_task/<int:id>', edit_task, name='edit_task'),
    path('delete_task/<int:id>', delete_task, name='delete_task'),
    path('tasks_done/', tasks_done, name='tasks_done'),
    path('tasks_failed/', tasks_failed, name='tasks_failed'),
    path('reminder/', reminder, name='reminder'),
]