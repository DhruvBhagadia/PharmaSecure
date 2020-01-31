from django.db import models

# Create your models here.

class Key(models.Model):
    medicine_name = models.CharField(max_length=100,default=None)
    privateKey_1 = models.CharField(max_length=500,default=None)
    privateKey_2 = models.CharField(max_length=500,default=None)
    publicKey = models.CharField(max_length=500,default=None)

    def __str__(self):
        return self.medicine_name


class Component(models.Model):
    key = models.ForeignKey(Key,on_delete=models.CASCADE)
    component_name = models.CharField(max_length=500,default=None)
    component_quantity= models.CharField(max_length=500,default=None)
    component_cost = models.CharField(max_length=500,default=None)

    def __str__(self):
        return self.component_name