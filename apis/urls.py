from django.urls import path
from . import views


urlpatterns = [
    path('', views.apiOverview, name="api-overview"),
    path('Todolist-all/', views.todoList, name="Todolist-all"),
    path('Todolist-detail/<str:pk>/', views.todoListDetail, name="Todolist-Detail"),
    path('Todolist-create/', views.todoListCreate, name="Todolist-Create"),
    path('Todolist-update/<str:pk>/', views.todoListUpdate, name="Todolist-update"),
    path('Todolist-delete/<str:pk>/', views.todoListDelete, name="Todolist-delete"),
]