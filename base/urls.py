from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login', views.CustomerLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(next_page='login'), name='logout'),
    path('register', views.RegisterPageView.as_view(), name='register'),
    
    path('', views.TaskListView.as_view(), name='tasks'),
    path('task/<int:pk>', views.DetailTaskView.as_view(), name='task'),
    path('task-create', views.TaskCreateView.as_view(), name='task-create'),
    path('task-update/<int:pk>', views.TaskUpdateView.as_view(), name='task-update'),
    path('task-delete/<int:pk>', views.TaskDeleteView.as_view(), name='task-delete'),
]
