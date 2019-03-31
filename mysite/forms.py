# coding=utf-8
from django import forms
from django.contrib.auth.models import User
from mysite.models import Profile, Post, Meter
from difflib import SequenceMatcher


class RegisterForm(forms.Form):
    username = forms.CharField(label=u"Имя пользователя")
    first_name = forms.CharField(label=u"Имя")
    last_name = forms.CharField(label=u"Фамилия")
    email = forms.EmailField(label=u"Email", required=True)
    room = forms.IntegerField(label='Квартира', required=True)
    password = forms.CharField(label=u"Пароль", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    def clean(self):
        max_similarity = 0.7
        min_password_length = 5
        cleaned_data = super(RegisterForm, self).clean()
        password_confirm = cleaned_data.get("password_confirm")
        password = cleaned_data.get("password")
        username = cleaned_data.get("username")
        room = cleaned_data.get("room")
        email = cleaned_data.get("email")

        email = User.objects.all().filter(email=email)
        if email:
            raise forms.ValidationError("Пользователь с таким адресом электронной почты уже существует.")

        user = User.objects.all().filter(username=username)
        print(user)
        if user:
            raise forms.ValidationError("Такой пользователь уже существует.")

        profile = Profile.objects.all().filter(room=room)
        if profile:
            raise forms.ValidationError("Номер квартиры уже есть в базе.")

        if password_confirm != password:
            # Only do something if both fields are valid so far.
            raise forms.ValidationError("Пароли не совпадают.")

        if SequenceMatcher(a=password.lower(), b=username.lower()).quick_ratio() > max_similarity \
                or len(password) < min_password_length:
            raise forms.ValidationError("Пароль слишком простой или совпадает с именем.")


        return cleaned_data



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author']

class MeterForm(forms.ModelForm):
    class Meta:
        model = Meter
        exclude = ['author']
