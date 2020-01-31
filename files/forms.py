from django import forms
from .models import Component,Key

class Medicine(forms.ModelForm):
    class Meta:
        model = Key
        fields = ('medicine_name',)


class Constituent(forms.ModelForm):
    class Meta:
        model = Component
        fields = ('component_name','component_cost','component_quantity',)