
from django import forms
from django.contrib.auth.models import User
from mysite.models import Profile, Post, Meter, Comment
from difflib import SequenceMatcher


class RegisterForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
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
        if user:
            raise forms.ValidationError("Пользователь с таким именем уже существует.")

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

class PostDeleteForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = []

    def clean(self):
        print('clean')
        cleaned_data = super(PostDeleteForm, self).clean()
        first = Post.objects.all().first()
        if first is None:
            raise forms.ValidationError("Нет сообщений.")
        if Comment.objects.filter(post=first.id).count() != 0:
            raise forms.ValidationError("Нельзя удалять сообщения с комментариями.")
        return cleaned_data


class MeterAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MeterAddForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Meter
        exclude = ['author']

    def clean_electric(self):
        electric = self.cleaned_data['electric']
        if electric is None:
            return electric
        if electric < 0:
            raise forms.ValidationError('Значение не должно быть отрицательными.')
        try:
            meter = Meter.objects.all().filter(author=self.request.user).latest('id')
            if electric < meter.electric:
                raise forms.ValidationError('Новое значение должно быть не меньше предыдущего.')
        except Meter.DoesNotExist:
            pass
        return electric

    def clean_cool(self):
        cool = self.cleaned_data['cool']
        if cool is None:
            return cool
        if cool < 0:
            raise forms.ValidationError('Значение не должно быть отрицательными.')
        try:
            meter = Meter.objects.all().filter(author=self.request.user).latest('id')
            if cool < meter.cool:
                raise forms.ValidationError('Новое значение должно быть не меньше предыдущего.')
        except Meter.DoesNotExist:
            pass
        return cool

    def clean_hot(self):
        hot = self.cleaned_data['hot']
        if hot is None:
            return hot
        if hot < 0:
            raise forms.ValidationError('Значение не должно быть отрицательными.')
        try:
            meter = Meter.objects.all().filter(author=self.request.user).latest('id')
            if hot < meter.hot:
                raise forms.ValidationError('Новое значение должно быть не меньше предыдущего.')
        except Meter.DoesNotExist:
            pass
        return hot



class MeterFilterForm(forms.Form):
    choices = [('1', 'Все'), ('2', 'Месяц'), ('3', 'Квартал'), ('4', 'Год'), ]
    rangechoice = forms.ChoiceField(widget=forms.Select(), choices=(choices), required=True, label='Диапазон')
    room = forms.ModelChoiceField(queryset=Profile.objects.all().order_by('-pk'), required=False, label='Квартира')
