from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'files'

urlpatterns = [
    path('ManagerRegister/', views.managerLogin, name='manLog'),
    path('AddEmployee/', views.addEmployee, name='addEmp'),
    path('see/', views.register, name='see'),
    # path('<int:med_id>/',views.add_component,name='constituent'),
    # path('list/',views.home,name='home'),
    # path('list/<int:id>/',views.retrieve_components,name='retrieve'),
]
