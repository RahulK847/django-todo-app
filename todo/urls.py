from django.urls import path
from .views import base, home
urlpatterns = [
    path('', base, name='base'),
    path('home/', home, name='home')
]