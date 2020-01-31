from django.contrib import admin
from django.urls import path,include
from . import views
app_name = 'files'
urlpatterns = [
    path('home/<int:id>',views.test,name='meds'),
    path('/',views.register_med,name='test'),
    path('<int:med_id>/',views.add_component,name='constituent'),
    path('list/',views.home,name='home'),
    path('list/<int:id>/',views.retrieve_components,name='retrieve'),
]
