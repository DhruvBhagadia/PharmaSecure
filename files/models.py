from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    email = models.EmailField(max_length=100, unique=True, default=None)
    name = models.CharField(max_length=100, default=None)
    manager_name = models.CharField(max_length=100,default=None)
    medicine_name = models.CharField(max_length=100,default=None)

    def __str__(self):
        return self.name

class Medicine(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    medicine_name = models.CharField(max_length=100, default=None)

    def __str__(self):
        return self.medicine_name

class Component(models.Model):
    key = models.ForeignKey(Medicine, on_delete=models.CASCADE, default=None)
    component_name = models.CharField(max_length=500,default=None)
    component_quantity= models.CharField(max_length=500, default=None)
    component_cost = models.CharField(max_length=500, default=None)  
    # def __str__(self):
    #     return self.component_name

class Log(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, default=None)
    component_name = models.CharField(max_length=500,default=None)
    component_quantity= models.CharField(max_length=500, default=None)
    component_cost = models.CharField(max_length=500, default=None)    

# class Key(models.Model):
#     medicine_name = models.CharField(max_length=100,default=None)
#     privateKey_1 = models.CharField(max_length=500,default=None)
#     privateKey_2 = models.CharField(max_length=500,default=None)
#     publicKey = models.CharField(max_length=500,default=None)

#     def __str__(self):
#         return self.medicine_name