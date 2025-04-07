from django import forms
from django.core.validators import MinValueValidator, RegexValidator

from agro.models import Cart, Complain, Order, ProductItem


class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductItem
        fields = ['category', 'title', 'description',
                 'image', 'price', 'quantity', 'unit', 'post_type']


class ComplainForm(forms.ModelForm):
    class Meta:
        model = Complain
        fields = ['subject', 'description']


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': '1', 'class': 'form-control'})
        }


class OrderForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Phone number must be 10 digits.',
                code='invalid_phone'
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    pincode = forms.CharField(
        max_length=6,
        validators=[
            RegexValidator(
                regex=r'^\d{6}$',
                message='Pincode must be 6 digits.',
                code='invalid_pincode'
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Order
        fields = [
            'full_name',
            'email',
            'phone',
            'address',
            'city',
            'state',
            'pincode'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not full_name or not full_name.strip():
            raise forms.ValidationError("Full name is required.")
        return full_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email or not email.strip():
            raise forms.ValidationError("Email is required.")
        return email
        