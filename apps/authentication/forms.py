# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from apps.home.models import Customer, CustomerContact, UserProfile, Department


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
    follower = forms.ModelChoiceField(queryset=UserProfile.objects.filter(department_id=2))

    class Meta:
        model = Customer
        fields = '__all__'


    # 如果有自定义的 clean 方法，请确保它不会阻止空值
    def clean(self):
        cleaned_data = super().clean()
        # 你的自定义逻辑
        return cleaned_data


class CustomerContactForm(forms.ModelForm):
    class Meta:
        model = CustomerContact
        fields = ['name', 'gender', 'position', 'phone_number']

class PasswordChangeForm(forms.Form):
    username = forms.CharField(max_length=150, label='用户名')
    verification_code = forms.CharField(max_length=50, label='公司内部验证码')
    new_password = forms.CharField(widget=forms.PasswordInput, label='新密码')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='确认新密码')

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("两次输入的密码不一致。")