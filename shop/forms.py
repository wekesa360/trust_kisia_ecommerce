
from django import forms
from captcha.fields import ReCaptchaField
from .models import DeliveryCharges
from captcha.widgets import ReCaptchaV2Checkbox

class CheckoutForm(forms.Form):
    # print(choices)
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'first',
        'id': 'first_name',
    }))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'last',
        'id': 'last_name',
    }))
    email_address = forms.EmailField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'name@website.com',
        'id': 'email_address',
    }))
    phone_number = forms.CharField(max_length=13, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '+254xxxxxxxxx',
    }))
    delivery_address = forms.ModelChoiceField(queryset=DeliveryCharges.objects.all(), widget=forms.Select(attrs={
        'id': 'address'
    }))    
    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    
    
    