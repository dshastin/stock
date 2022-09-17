from django import forms
from .models import Operation


class OperationForm(forms.ModelForm):
    class Meta:
        model = Operation
        fields = '__all__'
        widgets = {
            'portfolio': forms.Select(attrs={'class': 'form-control'}),
            'stock': forms.Select(attrs={'class': 'form-control'}),
            'order': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'datetime': forms.SelectDateWidget(attrs={'class': 'form-control'}),
        }
