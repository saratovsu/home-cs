"""
Тесты отображений, доступности только залогининым пользователям, перенаправлений

"""
from django.test import TestCase
from django.urls import reverse
from mysite.models import Profile, Meter
from django.contrib.auth.models import User


class TestRegistrationView(TestCase):
    """
    Тест регистрации
    """
    @classmethod
    def setUpTestData(cls):
        # Регистрация пользователя в Django и создание профиля
        for i in range(2):
            user = User.objects.create(username=f'test{i}',
                                       email=f'test{i}0@test.com',
                                       password='12345',
                                       first_name=f'firstname{i}',
                                       last_name=f'lastname{i}',
                                       is_active=True)
            profile = Profile.objects.create(user=user, room=i)
            for j in range(i + 1):
                meter = Meter.objects.create(author=user, electric=1.0, cool=1.0, hot=1.0)

        superuser = User.objects.create(username='root',
                                        email='root0@test.com',
                                        password='12345',
                                        first_name='firstrootname',
                                        last_name='lastrootname',
                                        is_active=True,
                                        is_staff=True,
                                        )



    def test_redirect_from_post_if_not_logged_in(self):
        # Тестирование перенаправления при попытке обращения к блогу
        # на страницу входа при отсутствии регистрации
        resp = self.client.get(reverse('post'))
        self.assertRedirects(resp, '/accounts/login/?next=/post/')

    def test_redirect_from_meter_if_not_logged_in(self):
        # Тестирование перенаправления при попытке обращения к странице передачи показаний
        # на страницу входа при отсутствии регистрации
        resp = self.client.get(reverse('meter'))
        self.assertRedirects(resp, '/accounts/login/?next=/meter/')

    def test_logged_in_uses_correct_template(self):
        # Проверка правильности шаблона логина и самого логина
        user = User.objects.get(id=1)
        self.client.force_login(user)
        resp = self.client.get(reverse('login'))

        # Проверка что пользователь залогинился
        self.assertEqual(str(resp.context['user']), 'test0')
        # Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)

        # Проверка того, что используется правильный шаблон
        self.assertTemplateUsed(resp, 'registration/login.html')

    def test_counts_meters_for_each_user(self):
        # Проверка доступности только своих записей

        # Для первого пользователя
        user = User.objects.get(id=1)
        self.client.force_login(user)
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(reverse('meter'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.context['meters'].paginated_rows) == 1)

        # Для второго пользователя
        user = User.objects.get(id=2)
        self.client.force_login(user)
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(reverse('meter'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.context['meters'].paginated_rows) == 2)



