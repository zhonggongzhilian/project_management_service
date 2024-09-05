# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from apps.home.models import Customer, CustomerContact


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "用户名",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "密码",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "用户名",
                "class": "form-control"
            }
        ))

    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "手机号",
                "class": "form-control"
            }
        ),
        validators=[
            # 你可以在这里添加手机号格式的验证
            # 例如：RegexValidator(r'^\d{11}$', '手机号格式不正确')
        ]
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "密码",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "再次输入密码",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'password1', 'password2')


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'address', 'phone', 'company_details']  # 添加 'company_details' 字段

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'company_details': forms.Textarea(attrs={'class': 'form-control', 'required': False})
            # 为 'company_details' 字段定义 widget
        }


class CustomerContactForm(forms.ModelForm):
    class Meta:
        model = CustomerContact
        fields = ['name', 'gender', 'position', 'phone_number']
