from django.contrib import admin
from .models import Task

# Register your models here.
admin.site.site_header = "Todo App Admin"
admin.site.site_title = "Todo App Admin Portal"
admin.site.index_title = "Welcome to the Todo App Admin Portal"
admin.site.register(Task)