from django import forms
from django.core.exceptions import ValidationError

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
