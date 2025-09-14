from django.urls import path
from . import views
urlpatterns = [
    path('', views.index , name='index'),
    path('task_entry/', views.add_task_page, name='task_entry'),
    path('task-delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('task-complete/<int:task_id>/', views.complete_task, name='complete_task'),
    # API endpoints
    path('api/tasks/', views.task_list_api, name='task_list_api'),
    path('api/tasks/<int:task_id>/', views.task_detail_api, name='task_detail_api'),
    
]
