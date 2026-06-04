from django.urls import path
from .views import home, signup_view, login_view, logout_view, add_task, complete_task, delete_task, task_history # ← import add_task

urlpatterns = [
    path('',          home,         name='home'),
    path('signup/',   signup_view,  name='signup'),
    path('login/',    login_view,   name='login'),
    path('logout/',   logout_view,  name='logout'),
    path('add-task/', add_task,     name='add_task'),   
    path('complete-task/<int:pk>',complete_task, name='complete_task' ),
    path('delete-task/<int:pk>', delete_task, name='delete_task'),
    path('task-history/', task_history, name='task_history'),

]