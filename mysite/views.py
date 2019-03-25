# coding=utf-8
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from .forms import RegisterForm, ProfileForm, PostForm
from .models import Profile, Post
from .filters import PostFilter


class LogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect("/")


class ProfileView(TemplateView):
    template_name = "registration/profile.html"

    def dispatch(self, request, *args, **kwargs):
        if not Profile.objects.filter(user=request.user).exists():
            return redirect(reverse("edit_profile"))
        context = {
            'selected_user': request.user
        }
        return render(request, self.template_name, context)


class RegisterView(TemplateView):
    template_name = "registration/register.html"

    def dispatch(self, request, *args, **kwargs):
        form = RegisterForm()
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                self.create_new_user(form)
                messages.success(request, u"Вы успешно зарегистрировались!")
                return redirect(reverse("login"))

        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def create_new_user(self, form):
        email = None
        if 'email' in form.cleaned_data:
            email = form.cleaned_data['email']
            User.objects.create_user(form.cleaned_data['username'],
                                     email, form.cleaned_data['password'],
                                     first_name=form.cleaned_data['first_name'],
                                     last_name=form.cleaned_data['last_name'])


class HomeView(TemplateView):
    template_name = "home.html"
    timeline_template_name = "timeline.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, self.template_name)

        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.author = request.user
                form.save()
                return redirect(reverse("home"))

        # date_list = ['month', 'year', 'all']
        # date_filter = PostFilter(request.GET, queryset=date_list)
        # f = PostFilter(request.GET,queryset=Post.objects.all().filter('datetime').order_by('-pk'))

        f = PostFilter(request.GET,queryset=Post.objects.all().filter(author=request.user).order_by('datetime'))
        context = {
            # 'posts': Post.objects.filter(author=request.user).order_by('datetime'),
            'filter': f,
            'posts': f.qs
        }
        return render(request, self.timeline_template_name, context)


class EditProfileView(TemplateView):
    template_name = "registration/edit_profile.html"

    def dispatch(self, request, *args, **kwargs):
        form = ProfileForm(instance=self.get_profile(request.user))
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=self.get_profile(request.user))
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                messages.success(request, u"Профиль успешно обновлен!")
                return redirect(reverse("profile"))
        return render(request, self.template_name, {'form': form})

    def get_profile(self, user):
        try:
            return user.profile
        except:
            return None


class ViewUserView(TemplateView):
    template_name = "registration/profile.html"

    def dispatch(self, request, *args, **kwargs):
        username = kwargs['username']
        try:
            user = User.objects.get(username=username)
            return render(request, self.template_name, {'selected_user': user})
        except:
            return redirect("/")

# def ViewPostFilter(request):
#     date_list = ['month', 'year', 'all']
#     date_filter = PostFilter(request.GET, queryset=date_list)
#     return render(request, 'search/user_list.html', {'filter': date_filter})