from django import forms
from .models import *

class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, label='Название истории')
    slug = forms.SlugField(max_length=255, label= 'URL')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols':60, 'rows': 10}),label='Текст истории')
    is_published = forms.BooleanField(label="Опубликовать", required=False, initial=True)
