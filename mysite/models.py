# coding=utf-8
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models

class Meter(models.Model):
    datetime = models.DateTimeField(verbose_name='Дата', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Собственник', related_name="meters")
    electric = models.FloatField(default=0, verbose_name='Электричество')
    cool = models.FloatField(default=0, verbose_name='Холодная вода')
    hot = models.FloatField(default=0, verbose_name='Горячая вода')

    def __str__(self):
        fieldsvalue = [str(getattr(self, field.name, '')) for field in self._meta.get_fields()]
        return ', '.join(fieldsvalue)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Собственник')
    room = models.IntegerField(default=0, blank=True, null=True, verbose_name='Квартира')

    def __str__(self):
        return f'{self.user.username}, {self.room} кв'


class Post(models.Model):
    datetime = models.DateTimeField(verbose_name='Дата', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Собственник', related_name="posts")
    text = models.CharField(max_length=1000, verbose_name=u"Текст", null=True, blank=True)

    class Meta:
        ordering = ["-datetime"]

    def __str__(self):
        fieldsvalue = [str(getattr(self, field.name, '')) for field in self._meta.get_fields()]
        return ', '.join(fieldsvalue)


class Comment(models.Model):
    datetime = models.DateTimeField(verbose_name='Дата', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Собственник', related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост', related_name="comments")
    text = models.CharField(max_length=1000, verbose_name='Сообщение', null=True, blank=True)

    class Meta:
        ordering = ["datetime"]

    def __str__(self):
        fieldsvalue = [str(getattr(self, field.name, '')) for field in self._meta.get_fields()]
        return ', '.join(fieldsvalue)
















