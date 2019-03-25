"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView

from mysite.views import HomeView, LogoutView, RegisterView, ProfileView, EditProfileView
from mysite.views import ViewUserView #, PostView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name="home"),

    url(r'^accounts/login/$', LoginView.as_view(template_name='registration/login.html'), name="login"),
    url(r'^accounts/logout/$', LogoutView.as_view(), name="logout"),
    url(r'^accounts/register/$', RegisterView.as_view(), name="register"),
    url(r'^accounts/profile/$', ProfileView.as_view(), name="profile"),
    url(r'^accounts/profile/edit/$', EditProfileView.as_view(), name="edit_profile"),

    url(r'^user/@(?P<username>[-\w\s\d]+)$', ViewUserView.as_view(), name="view_user"),

    url(r'^admin/', admin.site.urls),
]
