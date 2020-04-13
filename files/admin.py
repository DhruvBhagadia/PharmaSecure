from django.contrib import admin
from .models import Employee, Medicine, Component, Log
# Register your models here.

admin.site.register(Employee)
admin.site.register(Medicine)
admin.site.register(Component)
admin.site.register(Log)