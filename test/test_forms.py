"""
Тестирование форм:
"""

from django.test import TestCase
from django.test.client import RequestFactory

from django.contrib.auth.models import User
from mysite.forms import RegisterForm, MeterAddForm, MeterFilterForm, PostDeleteForm
from mysite.models import Profile, Meter, Post, Comment



class Test_RegisterForm(TestCase):
    """
    Тестирование формы регистрации
    """

    @classmethod
    def setUpTestData(cls):
        #Регистрация пользователя в Django и создание профиля
        user = User.objects.create(username='test0',
                            email='test0@test.com',
                            password='test0',
                            first_name='firstname0',
                            last_name='lastname0')
        Profile.objects.create(user=user, room=0)

    def test_renew_form_username_field_label(self):
        #Проверка названия поля username на форме
        form = RegisterForm()
        self.assertEqual(form.fields['username'].label, 'Имя пользователя')

    def test_renew_form_first_name_field_label(self):
        #Проверка названия поля first_name на форме
        form = RegisterForm()
        self.assertEqual(form.fields['first_name'].label, 'Имя')

    def test_renew_form_last_name_field_label(self):
        #Проверка названия поля last_name на форме
        form = RegisterForm()
        self.assertEqual(form.fields['last_name'].label, 'Фамилия')

    def test_renew_form_email_field_label(self):
        #Проверка названия поля email на форме
        form = RegisterForm()
        self.assertEqual(form.fields['email'].label, 'Email')

    def test_renew_form_room_field_label(self):
        #Проверка названия поля room на форме
        form = RegisterForm()
        self.assertEqual(form.fields['room'].label, 'Квартира')

    def test_renew_form_password_field_label(self):
        #Проверка названия поля password на форме
        form = RegisterForm()
        self.assertEqual(form.fields['password'].label, 'Пароль')

    def test_renew_form_password_confirm_field_label(self):
        #Проверка названия поля password_confirm на форме
        form = RegisterForm()
        self.assertEqual(form.fields['password_confirm'].label, 'Подтвердите пароль')

    def test_renew_form_username_exist(self):
        #Проверка повторной регистрации с существующим username
        form_data = {
            'username': 'test0',
            'first_name': 'first_name1',
            'last_name': 'last_name1',
            'email': 'test1@test.com',
            'room': '1',
            'password': '12345',
            'password_confirm': '12345',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'], [str(User._meta.get_field('username').error_messages['unique'])])

    def test_renew_form_email_exist(self):
        # Проверка повторной регистрации с существующим email
        form_data = {
            'username': 'test1',
            'first_name': 'first_name1',
            'last_name': 'last_name1',
            'email': 'test0@test.com',
            'room': '1',
            'password': '12345',
            'password_confirm': '12345',
        }
        form = RegisterForm(data=form_data)
        self.assertEqual(form.errors['__all__'], ['Пользователь с таким адресом электронной почты уже существует.'])
        self.assertFalse(form.is_valid())

    def test_renew_form_room_exist(self):
        # Проверка повторной регистрации с существующим room
        form_data = {
            'username': 'test1',
            'first_name': 'first_name1',
            'last_name': 'last_name1',
            'email': 'test1@test.com',
            'room': '0',
            'password': '12345',
            'password_confirm': '12345',
        }
        form = RegisterForm(data=form_data)
        self.assertEqual(form.errors['__all__'], ['Номер квартиры уже есть в базе.'])
        self.assertFalse(form.is_valid())

    def test_renew_form_passwords_notequal(self):
        #Проверка на несовпадение паролей
        form_data = {
            'username': 'test1',
            'first_name': 'first_name1',
            'last_name': 'last_name1',
            'email': 'test1@test.com',
            'room': '1',
            'password': '12345',
            'password_confirm': '12344',
        }
        form = RegisterForm(data=form_data)
        self.assertEqual(form.errors['__all__'], ['Пароли не совпадают.'])
        self.assertFalse(form.is_valid())

    def test_renew_form_password_is_easy(self):
        #Проверка на сложность пароля
        form_data = {
            'username': 'test1',
            'first_name': 'first_name1',
            'last_name': 'last_name1',
            'email': 'test1@test.com',
            'room': '1',
            'password': 'test12',
            'password_confirm': 'test12',
        }
        form = RegisterForm(data=form_data)
        self.assertEqual(form.errors['__all__'], ['Пароль слишком простой или совпадает с именем.'])
        self.assertFalse(form.is_valid())


class Test_MeterNegativeAddForm(TestCase):
    """
    Тестирование формы Meter на ввод отрицательных значений
    """

    @classmethod
    def setUpTestData(cls):
        # Регистрация пользователя в Django и создание профиля
        user = User.objects.create(username='test0',
                                   email='test0@test.com',
                                   password='test0',
                                   first_name='firstname',
                                   last_name='lastname')
        profile = Profile.objects.create(user=user, room=0)

    def setUp(self):
        self.factory = RequestFactory()

    def test_electric_add_negative(self):
        #Проверка на неотрицательность поля electric
        form_data = {
            'electric': -1,
            'cool': 1.0,
            'hot': 1.0,
        }
        request = self.factory.get('/')
        request.user = User.objects.get(pk=1)
        form = MeterAddForm(data=form_data, request=request)
        self.assertEqual(form.errors['electric'], ['Значение не должно быть отрицательными.'])
        self.assertFalse(form.is_valid())

    def test_cool_add_negative(self):
        # Проверка на неотрицательность поля cool
        form_data = {
            'electric': 1.0,
            'cool': -1.0,
            'hot': 1.0,
        }
        request = self.factory.get('/')
        request.user = User.objects.get(pk=1)
        form = MeterAddForm(data=form_data, request=request)
        self.assertEqual(form.errors['cool'], ['Значение не должно быть отрицательными.'])
        self.assertFalse(form.is_valid())

    def test_hot_add_negative(self):
        # Проверка на неотрицательность поля hot
        form_data = {
            'electric': 1.0,
            'cool': 1.0,
            'hot': -1.0,
        }
        request = self.factory.get('/')
        request.user = User.objects.get(pk=1)
        form = MeterAddForm(data=form_data, request=request)
        self.assertEqual(form.errors['hot'], ['Значение не должно быть отрицательными.'])
        self.assertFalse(form.is_valid())


class Test_MeterAddForm(TestCase):
    """
    Тестирование формы Meter на ввод значений меньше чем предыдущее
    """

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='test0',
                                   email='test0@test.com',
                                   password='test0',
                                   first_name='firstname',
                                   last_name='lastname')
        profile = Profile.objects.create(user=user, room=0)
        meter = Meter.objects.create(author=user, electric=1.0, cool=1.0, hot=1.0)

    def setUp(self):
        self.factory = RequestFactory()

    def test_electric_add_less_then_last(self):
        #Проверка на неуменьшающееся значение поля electric
        form_data = {
            'electric': 0.5,
            'cool': 1.0,
            'hot': 1.0,
        }
        request = self.factory.get('/')
        request.user = User.objects.get(pk=1)
        form = MeterAddForm(data=form_data, request=request)
        self.assertEqual(form.errors['electric'], ['Новое значение должно быть не меньше предыдущего.'])
        self.assertFalse(form.is_valid())

    def test_cool_add_less_then_last(self):
        # Проверка на неуменьшающееся значение поля cool
        form_data = {
            'electric': 1.1,
            'cool': 0.5,
            'hot': 1.0,
        }
        request = self.factory.get('/')
        request.user = User.objects.get(pk=1)
        form = MeterAddForm(data=form_data, request=request)
        self.assertEqual(form.errors['cool'], ['Новое значение должно быть не меньше предыдущего.'])
        self.assertFalse(form.is_valid())

    def test_hot_add_less_then_last(self):
        # Проверка на неуменьшающееся значение поля hot
        form_data = {
            'electric': 1.1,
            'cool': 1.5,
            'hot': 0.9,
        }
        request = self.factory.get('/')
        request.user = User.objects.get(pk=1)
        form = MeterAddForm(data=form_data, request=request)
        self.assertEqual(form.errors['hot'], ['Новое значение должно быть не меньше предыдущего.'])
        self.assertFalse(form.is_valid())



