# coding=utf-8
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models

class Meter(models.Model):
    datetime = models.DateTimeField(verbose_name='Дата', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=u"Автор", related_name="meters")
    electric = models.FloatField(default=0.0, verbose_name='Электричество')
    cool = models.FloatField(default=0.0, verbose_name='Холодная вода')
    hot = models.FloatField(default=0.0, verbose_name='Горячая вода')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Собственник')
    room = models.IntegerField(default=0, blank=True, null=True, verbose_name='Квартира')


class Post(models.Model):
    datetime = models.DateTimeField(verbose_name=u"Дата", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=u"Автор", related_name="posts")
    text = models.CharField(max_length=1000, verbose_name=u"Текст", null=True, blank=True)

    class Meta:
        ordering = ["-datetime"]


class Comment(models.Model):
    datetime = models.DateTimeField(verbose_name=u"Дата", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=u"Автор", related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=u"Пост", related_name="comments")
    text = models.CharField(max_length=1000, verbose_name=u"Текст", null=True, blank=True)

    class Meta:
        ordering = ["datetime"]

















