from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from .models import User_info


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom password validation message
        self.fields['password1'].help_text = "Your password must contain at least 8 characters, including one uppercase letter."
        
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isupper() for char in password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        return password
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

class UserInfo(forms.ModelForm):
    # user = forms.CharField(widget=forms.TextInput(attrs={'type':'hidden'}))
    class Meta:
        model = User_info
        fields = ('profile_pic','gender','address','phone')


class UserFLEname(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email')