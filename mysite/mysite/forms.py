from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label="帳號",
     widget=forms.TextInput(
         attrs={'class':'form-control','placeholder':'請輸入用戶名'}))
    password = forms.CharField(label="密碼", 
    widget=forms.PasswordInput(
        attrs={'class':'form-control'}))
    
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('帳號或密碼不正確')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

class RegForm(forms.Form):
    username = forms.CharField(label="帳號",
    max_length=30,
    min_length=3,
    widget=forms.TextInput(
    attrs={'class':'form-control','placeholder':'請輸入3-30位用戶名'}))

    email = forms.EmailField(label="Email",
    widget=forms.EmailInput(
    attrs={'class':'form-control','placeholder':'請輸入電子郵件'}))
     
    
    password = forms.CharField(label="密碼", 
                               min_length=6,
                               widget=forms.PasswordInput(
                               attrs={'class':'form-control','placeholder':'請輸入密碼'}))

    password_again = forms.CharField(label="再輸入一次密碼", 
                               min_length=6,
                               widget=forms.PasswordInput(
                               attrs={'class':'form-control','placeholder':'再輸入一次密碼'}))
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用戶名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('電子郵件地址已被使用')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('兩次輸入密碼不一致')
        return password_again