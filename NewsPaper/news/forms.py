from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    title = forms.CharField(min_length=15)

    class Meta:
        model = Post
        fields = ['author', 'title', 'postCategory', 'text']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")

        if title[0].islower():
            raise ValidationError(
                "Заголовок должен начинаться с заглавной буквы."
            )

        return cleaned_data


class PostArForm(forms.ModelForm):
    title = forms.CharField(min_length=15)

    class Meta:
        model = Post
        fields = ['author', 'title', 'postCategory', 'text']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")

        if title[0].islower():
            raise ValidationError(
                "Заголовок должен начинаться с заглавной буквы."
            )

        return cleaned_data
