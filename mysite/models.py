# coding=utf-8
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=u"Пользователь")
    room = models.CharField(max_length=30, blank=True, null=True, verbose_name=u"Квартира")


class Post(models.Model):
    datetime = models.DateTimeField(verbose_name=u"Дата", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=u"Автор", related_name="posts")
    electric = models.IntegerField(null=False, blank=False, default=0)
    cool = models.IntegerField(null=False, blank=False, default=0)
    hot = models.IntegerField(null=False, blank=False, default=0)

    def __str__(self):
        return (f'Электричество: {self.electric} квт/ч, холодная вода: {self.cool} м3, горячая вода: {self.hot} м3')
    class Meta:
        ordering = ["-datetime"]


















