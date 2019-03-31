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

from mysite.forms import RegisterForm, PostForm, MeterForm
#ProfileForm
from mysite.models import Profile, Post, Comment, Meter


class LogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect("/")


class MeterView(TemplateView):
    template_name = "meter.html"

    def dispatch(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     return render(request, self.template_name)
        form = MeterForm()
        if request.method == 'POST':
            form = MeterForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.author = request.user
                form.save()
                return redirect(reverse("meter"))
        if request.user.is_superuser:
            meters = Meter.objects.all().order_by('-pk')
        else:
            meters = Meter.objects.all().filter(author=request.user).order_by('-pk')
        context = {
            'meters': meters
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
            else:
                messages.error(request, 'The form is invalid.')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def create_new_user(self, form):
        email = None
        if 'email' in form.cleaned_data:
            email = form.cleaned_data['email']
            user = User.objects.create_user(form.cleaned_data['username'],
                                     email, form.cleaned_data['password'],
                                     first_name=form.cleaned_data['first_name'],
                                     last_name=form.cleaned_data['last_name'])
            Profile.objects.create(user=user, room=form.cleaned_data['room'])


class PostView(TemplateView):
    timeline_template_name = "post.html"

    def dispatch(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     return render(request, self.template_name)

        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.author = request.user
                form.save()
                return redirect(reverse("post"))
        if request.user.is_superuser:
            post = Post.objects.all()
        else:
            post = Post.objects.all().filter(author=request.user)
        context = {
            'posts': post
        }
        return render(request, self.timeline_template_name, context)


class PostCommentView(View):
    def dispatch(self, request, *args, **kwargs):
        post_id = request.GET.get("post_id")
        comment = request.GET.get("comment")
        if comment and post_id:
            post = Post.objects.get(pk=post_id)
            comment = Comment(text=comment, post=post, author=request.user)
            comment.save()
            return render(request, "blocks/comment.html", {'comment': comment})
        return HttpResponse(status=500, content="")


class HomeView(TemplateView):
    template_name = "home.html"
