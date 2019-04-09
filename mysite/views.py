# coding=utf-8
import datetime
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django_tables2 import RequestConfig
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, PostForm, MeterAddForm, MeterFilterForm
#ProfileForm
from .models import Profile, Post, Comment, Meter
from .tables import MeterTable


class LogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect("/")


class MeterView(TemplateView):
    template_name = "meter.html"

    def dispatch(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     return render(request, self.template_name)
        addform = MeterAddForm(request.POST or None, request=request)

        filterform = MeterFilterForm(request.POST or None,
                                     initial={'rangechoice':request.session.get('rangechoice',1),
                                              'room':request.session.get('room'),
                                              })
        if request.method == 'POST':
            if 'electric' in request.POST and addform.is_valid():
                addform.instance.author = request.user
                addform.save()
                return redirect(reverse("meter"))
            if 'room' in request.POST and filterform.is_valid():
                request.session['rangechoice'] = filterform['rangechoice'].value()
                if not request.user.is_superuser:
                    request.session['room'] = None
                else:
                    request.session['room'] = filterform['room'].value()
                return redirect(reverse("meter"))

        if request.user.is_superuser:
            print(request.session.get('room'))
            meters = Meter.objects.all()
            meters = self.filter_by_choice(meters, request.session.get('rangechoice', 1))
            meters = self.filter_by_name(meters, request.session.get('room')).order_by('-pk')
        else:
            meters = Meter.objects.all().filter(author=request.user)
            meters = self.filter_by_choice(meters, request.session.get('rangechoice',1)).order_by('-pk')

        table = MeterTable(meters)
        RequestConfig(request).configure(table)

        context = {
            'addform': addform,
            'filterform': filterform,
            'meters': table
        }
        return render(request, self.template_name, context)

    def filter_by_name(self, input, room):
        if room == '' or room is None:
            return input
        try:
            user = Profile.objects.get(id=room).user
            return input.filter(author=user)
        except:
            return input

    def filter_by_choice(self, input, choice=1):
        now = datetime.datetime.now()
        if choice == '1':
            return input
        elif choice == '2':
            dt = now - datetime.timedelta(days=30)
        elif choice == '3':
            dt = now - datetime.timedelta(days=30*4)
        elif choice == '4':
            dt = now - datetime.timedelta(days=365)
            # dt = now - datetime.timedelta(minutes=2)
        else:
            return input
        return input.filter(datetime__gte=dt)


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
            if 'text' in request.POST:
                form = PostForm(request.POST, request.FILES)
                if form.is_valid():
                    form.instance.author = request.user
                    form.save()
                    return redirect(reverse("post"))
            else:
                first = Post.objects.all().first()
                if first is not None:
                        if Comment.objects.filter(post=first.id).count() == 0:
                            first.delete()

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
