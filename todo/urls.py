from django.urls import path
from .views import home, signup_view, login_view, logout_view, add_task  # ← import add_task

urlpatterns = [
    path('',          home,         name='home'),
    path('signup/',   signup_view,  name='signup'),
    path('login/',    login_view,   name='login'),
    path('logout/',   logout_view,  name='logout'),
    path('add-task/', add_task,     name='add_task'),   
]