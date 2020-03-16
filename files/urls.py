from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'files'

urlpatterns = [
    path('managerRegister/', views.managerLogin, name='manLog'),
    path('addEmployee/', views.addEmployee, name='addEmp'),
    path('display/', views.display, name='display'),
    path('medicineName/', views.medicineName, name='medName'),
    path('employee/', views.addComponent, name='addComp'),
    # path('<int:med_id>/',views.add_component,name='constituent'),
    # path('list/',views.home,name='home'),
    # path('list/<int:id>/',views.retrieve_components,name='retrieve'),
]
