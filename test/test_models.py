"""
Тестирование моделей: названй меток, длины полей, функций __str__
"""

from django.test import TestCase
from django.contrib.auth.models import User
from mysite.models import Profile, Post, Comment, Meter


class ProfileModelTest(TestCase):
    """
    Тестирование модели Profile (названия меток полей и getstr)
    """

    filds_name = {
        'user': 'Собственник',
        'room': 'Квартира',
    }

    model = Profile

    @classmethod
    def setUpTestData(cls):
        #Регистрация пользователя в Django и создание профиля
        user = User.objects.create(username='test0',
                            email='test0@test.com',
                            password='test0',
                            first_name='firstname',
                            last_name='lastname')
        Profile.objects.create(user=user, room=0)

    def test_labels(self):
        #Проверка меток полей
        object = self.model.objects.get(id=1)
        for key, val in self.filds_name.items():
            field_label = object._meta.get_field(key).verbose_name
            self.assertEquals(field_label,val)

    def test_getstr(self):
        #Проверка __str__
        object = self.model.objects.get(id=1)
        self.assertEquals(str(object), str(object.room))


class PostModelTest(TestCase):
    """
    Тестирование модели Post (названия меток и длины полей)
    """

    filds_name = {
        'datetime': 'Дата',
        'author': 'Собственник',
        'text': 'Сообщение',
    }

    model = Post

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='test0',
                            email='test0@test.com',
                            password='test0',
                            first_name='firstname',
                            last_name='lastname')
        Profile.objects.create(user=user, room=0)
        Post.objects.create(author=user, text='text0')

    def test_text_max_length(self):
        #Проверка длины поля text
        author = self.model.objects.get(id=1)
        max_length = author._meta.get_field('text').max_length
        self.assertEquals(max_length, 100)

    def test_labels(self):
        #Проверка меток полей
        object = self.model.objects.get(id=1)
        for key, val in self.filds_name.items():
            field_label = object._meta.get_field(key).verbose_name
            self.assertEquals(field_label,val)


class CommentModelTest(TestCase):
    """
    Тестирование модели Comment (названия меток и длины полей)
    """

    filds_name = {
        'datetime': 'Дата',
        'author': 'Собственник',
        'post': 'Сообщение',
        'text': 'Комментарий',
    }

    model = Comment

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='test0',
                            email='test0@test.com',
                            password='test0',
                            first_name='firstname',
                            last_name='lastname')
        Profile.objects.create(user=user, room=0)
        post = Post.objects.create(author=user, text='text0')
        Comment.objects.create(author=user, post=post, text='comment1')
        Comment.objects.create(author=user, post=post, text='comment2')

    def test_text_max_length(self):
        # Проверка длины поля text
        author = self.model.objects.get(id=1)
        max_length = author._meta.get_field('text').max_length
        self.assertEquals(max_length, 100)

    def test_labels(self):
        #Проверка меток полей
        object = self.model.objects.get(id=1)
        for key, val in self.filds_name.items():
            field_label = object._meta.get_field(key).verbose_name
            self.assertEquals(field_label, val)


class MetertModelTest(TestCase):
    """
    Тестирование модели Comment (названия меток и длины полей)
    """

    filds_name = {
        'datetime': 'Дата',
        'author': 'Собственник',
        'electric': 'Электричество',
        'cool': 'Холодная вода',
        'hot': 'Горячая вода',
    }

    model = Meter

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='test0',
                            email='test0@test.com',
                            password='test0',
                            first_name='firstname',
                            last_name='lastname')
        Profile.objects.create(user=user, room=0)
        Meter.objects.create(author=user, electric=1.0, cool=1.0, hot=1.0)

    def test_labels(self):
        #Проверка меток полей
        object = self.model.objects.get(id=1)
        for key, val in self.filds_name.items():
            field_label = object._meta.get_field(key).verbose_name
            self.assertEquals(field_label, val)


