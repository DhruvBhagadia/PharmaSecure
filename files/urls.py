from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'files'

urlpatterns = [
    path('managerRegister/', views.managerRegister, name='manReg'),
    path('managerLogin/', views.managerLogin, name='manLog'),
    path('employeeLogin/', views.employeeLogin, name='empLog'),
    path('newPassword/', views.newPassword, name='newPass'),
    path('addEmployee/', views.addEmployee, name='addEmp'),
    path('logs/', views.logs, name='logs'),
    path('display/', views.display, name='display'),
    path('medicineName/', views.medicineName, name='logout'),
    path('employee/<int:employee_id>/', views.addComponent, name='addComponent'),

    # path('<int:med_id>/',views.add_component,name='constituent'),
    # path('list/',views.home,name='home'),
    # path('list/<int:id>/',views.retrieve_components,name='retrieve'),
]
