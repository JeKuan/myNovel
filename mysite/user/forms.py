from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username_or_email = forms.CharField(label="帳號或電子郵件",
     widget=forms.TextInput(
         attrs={'class':'form-control','placeholder':'請輸入用戶名或電子郵件'}))
    password = forms.CharField(label="密碼", 
    widget=forms.PasswordInput(
        attrs={'class':'form-control'}))
    
    def clean(self):
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username_or_email, password=password)
        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username, password=password)
                if not user is None:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
               
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
    
    verification_code = forms.CharField(label="驗證碼",
    required=False,
    widget=forms.TextInput(
    attrs={'class':'form-control','placeholder':'點擊「發送驗證碼」到郵箱'}))
    
    password = forms.CharField(label="密碼", 
                               min_length=6,
                               widget=forms.PasswordInput(
                               attrs={'class':'form-control','placeholder':'請輸入密碼'}))

    password_again = forms.CharField(label="再輸入一次密碼", 
                               min_length=6,
                               widget=forms.PasswordInput(
                               attrs={'class':'form-control','placeholder':'再輸入一次密碼'}))
    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegForm, self).__init__(*args, **kwargs)


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

    def clean(self):
        #判斷驗證碼
        code = self.request.session.get('register_code','')
        verification_code = self.cleaned_data.get('verification_code','').strip()
        if code == '' or code != verification_code:
            raise forms.ValidationError('驗證碼不正確')
        return self.cleaned_data


    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code','').strip()
        if verification_code == '':
            raise forms.ValidationError('驗證碼不得為空')
        return verification_code

class ChangeNicknameForm(forms.Form):
    nickname_new = forms.CharField(label="新的暱稱",
    max_length=20,
    widget=forms.TextInput(
    attrs={'class':'form-control','placeholder':'請輸入新的暱稱'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeNicknameForm, self).__init__(*args, **kwargs)


    def clean(self):
        #判斷用戶是否登入
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用戶尚未登入')   
        return self.cleaned_data
   
    def clean_nickname_new(self):
        nickname_new = self.cleaned_data.get('nickname_new','').strip()
        if nickname_new == '':
            raise forms.ValidationError('新的暱稱不能為空')
        else:
            return nickname_new

class BindEmailForm(forms.Form):
    email = forms.EmailField(label="郵箱",
    widget=forms.EmailInput(
    attrs={'class':'form-control','placeholder':'請輸入正確的郵箱'}))
    verification_code = forms.CharField(label="驗證碼",
    required=False,
    widget=forms.TextInput(
    attrs={'class':'form-control','placeholder':'點擊「發送驗證碼」到郵箱'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailForm, self).__init__(*args, **kwargs)


    def clean(self):
        #判斷用戶是否登入
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用戶尚未登入')   
       

        #判斷用戶是否已經綁定
        if self.request.user.email != '':
            raise forms.ValidationError('已完成郵箱綁定')

        #判斷驗證碼
        code = self.request.session.get('bind_email_code','')
        verification_code = self.cleaned_data.get('verification_code','').strip()
        if code == '' or code != verification_code:
            raise forms.ValidationError('驗證碼不正確')

        return self.cleaned_data

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code','').strip()
        if verification_code == '':
            raise forms.ValidationError('驗證碼不得為空')
        return verification_code

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('該郵箱已綁定')
        return email

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label="舊的密碼", 
    widget=forms.PasswordInput(
        attrs={'class':'form-control','placeholder':'請輸入舊的密碼'}))

    new_password = forms.CharField(label="新的密碼", 
    widget=forms.PasswordInput(
        attrs={'class':'form-control','placeholder':'請輸入新的密碼'}))

    new_password_again = forms.CharField(label="確認密碼", 
    widget=forms.PasswordInput(
        attrs={'class':'form-control','placeholder':'請再次輸入新的密碼'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        #驗證新的密碼是否一致
        new_password = self.cleaned_data.get('new_password','').strip()
        new_password_again = self.cleaned_data.get('new_password_again','').strip()
        if new_password != new_password_again or new_password == '':
            raise forms.ValidationError('兩次輸入密碼不一致')

        return self.cleaned_data
   
    def clean_old_password(self):
        #驗證舊的密碼是否正確
        old_password = self.cleaned_data.get('old_password','').strip()
        if not self.user.check_password(old_password):
            raise forms.ValidationError('舊的密碼不正確')
        else:
            return old_password

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="郵箱",
    widget=forms.EmailInput(
    attrs={'class':'form-control','placeholder':'請輸入備援郵箱'}))

    verification_code = forms.CharField(label="驗證碼",
    required=False,
    widget=forms.TextInput(
    attrs={'class':'form-control','placeholder':'點擊「發送驗證碼」到郵箱'}))
    
    new_password = forms.CharField(label="新的密碼", 
    widget=forms.PasswordInput(
    attrs={'class':'form-control','placeholder':'請輸入新的密碼'}))
    
    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('該郵箱不存在')
        return email
       

    def clean_verification_code(self):

        verification_code = self.cleaned_data.get('verification_code','').strip()
        if verification_code == '':
            raise forms.ValidationError('驗證碼不得為空')
        #判斷驗證碼
        code = self.request.session.get('forgot_password_code','')
        verification_code = self.cleaned_data.get('verification_code','').strip()
        if code == '' or code != verification_code:
            raise forms.ValidationError('驗證碼不正確')        
        return verification_code