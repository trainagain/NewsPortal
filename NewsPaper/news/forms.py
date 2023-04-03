from django import forms
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

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


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        common_users = Group.objects.get(name="common users")
        user.groups.add(common_users)
        return user
