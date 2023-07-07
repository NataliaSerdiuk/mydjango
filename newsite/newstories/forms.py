from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import CaptchaField

from .models import *


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Stories
        fields = ['title', 'slug', 'content', 'photo', 'is_published']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_content(self):
        content = self.cleaned_data['content']
        user_text_list_content = content.lower().split()
        with open('D:/Python/djangosite/newsite/newstories/resources/forbidden_words.txt', 'r',
                  encoding='utf-8') as file:
            forbidden_words = [word.strip() for word in file.readlines() if word.strip()]
            for word in user_text_list_content:
                if word.lower() in forbidden_words:
                    raise ValidationError("Текст содержит недопустимое слово.")
                return content

    def clean_title(self):
        title = self.cleaned_data['title']
        user_text_list_title = title.lower().split()
        with open('D:/Python/djangosite/newsite/newstories/resources/forbidden_words.txt', 'r',
                  encoding='utf-8') as file:
            forbidden_words = [word.strip() for word in file.readlines() if word.strip()]
            for word in user_text_list_title:
                if word.lower() in forbidden_words:
                    raise ValidationError("Заголовок содержит недопустимое слово.")
                return title


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(label='Твоё имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    class Meta:
        model = User
        fields = ('first_name', 'username','email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    subject = forms.CharField(label='Тема', max_length=100)
    content = forms.CharField(widget=forms.Textarea(attrs={'cols':60,'rows': 10}), label='Сообщение')
    captcha = CaptchaField()