from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    email = models.CharField(max_length=100, default=None)
    name = models.EmailField(max_length=100, default=None)

    def __str__(self):
        return self.user

class Medicine(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    medicine_name = models.CharField(max_length=100, default=None)

    def __str__(self):
        return self.medicine_name

class Component(models.Model):
    # key = models.ForeignKey(Medicine, on_delete=models.CASCADE, default=None)
    component_name = models.CharField(max_length=500,default=None)
    component_quantity= models.CharField(max_length=500, default=None)
    component_cost = models.CharField(max_length=500, default=None)  
    # def __str__(self):
    #     return self.component_name

# class Key(models.Model):
#     medicine_name = models.CharField(max_length=100,default=None)
#     privateKey_1 = models.CharField(max_length=500,default=None)
#     privateKey_2 = models.CharField(max_length=500,default=None)
#     publicKey = models.CharField(max_length=500,default=None)

#     def __str__(self):
#         return self.medicine_name