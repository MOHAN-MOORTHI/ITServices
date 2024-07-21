from django import forms
from django.contrib.auth.models import User
from django import forms
from .models import Service

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    password = forms.CharField(widget=forms.PasswordInput())

class OTPForm(forms.Form):
    otp = forms.IntegerField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())



class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['service_name', 'payment_terms', 'service_price', 'service_package', 'service_tax', 'service_image', 'active']
