from django import forms
from .models import Employee
from django.contrib.auth.models import User

# class Medicine(forms.ModelForm):
#     class Meta:
#         model = Key
#         fields = ('medicine_name',)


# class Constituent(forms.ModelForm):
#     class Meta:
#         model = Component
#         fields = ('component_name','component_cost','component_quantity',)	

class ManagerForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ('username', 'password',)
		help_texts = {'username': None, 'password': None}