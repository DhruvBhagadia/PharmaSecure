from django.contrib import admin
from .models import Employee, Medicine, Component
# Register your models here.

admin.site.register(Employee)
admin.site.register(Medicine)
admin.site.register(Component)