from django import forms
from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    username = forms.CharField(label='名稱', max_length=15)
    password = forms.CharField(label='密碼', max_length=20, widget=forms.PasswordInput)
    captcha = CaptchaField(label='驗證碼')

class RegisterForm(forms.Form):
    username = forms.CharField(label='使用者名稱', max_length=15)
    password = forms.CharField(label='輸入密碼', max_length=20, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='確認密碼', max_length=20, widget=forms.PasswordInput)
    captcha = CaptchaField(label='驗證碼')

class GuessForm(forms.Form):
    guess_word = forms.CharField(label='輸入五個字母的單字', max_length=5)
