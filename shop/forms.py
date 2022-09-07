from django import forms


class CheckoutForm(forms.Form):

    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'first_name',
    }))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'last_name',
    }))
    email_address = forms.EmailField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'john@website.com',
        'id': 'email_address',
    }))
    phone_number = forms.CharField(max_length=13, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '+254xxxxxxxxx',
    }))
    delivery_address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '1234 Main St',
        'id': 'address'
    }))