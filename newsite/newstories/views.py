from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm


from .forms import *
from .models import *
from .utils import *



class StoriesHomepage(DataMixin, ListView):
    model = Stories
    template_name = 'newstories/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = "Главная страница",posts_selected=0)
        return dict(list(context.items()) + list(c_def.items()))


    def get_queryset(self):
        return Stories.objects.filter(is_published = True)

class StoriesBestRating(DataMixin, ListView):
    model = LikeDislike
    template_name = 'newstories/best.html'
    context_object_name = 'posts'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Лучшие истории", vote_selected=1)
        return dict(list(context.items()) + list(c_def.items()))
    def get_queryset(self):
        return Stories.objects.annotate(rating=Sum('likedislike__vote')).order_by('-rating').filter(rating__gt=0)

class StoriesWorstRating(DataMixin, ListView):
    model = LikeDislike
    template_name = 'newstories/worst.html'
    context_object_name = 'posts'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Скучные истории",vote_selected=-1)
        return dict(list(context.items()) + list(c_def.items()))
    def get_queryset(self):
        return Stories.objects.annotate(rating=Sum('likedislike__vote')).order_by('-rating').filter(rating__lt=1)

class StoriesNoRating(DataMixin, ListView):
    model = LikeDislike
    template_name = 'newstories/no_vote.html'
    context_object_name = 'posts'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Неоцененные истории", vote_selected=0)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Stories.objects.filter(likedislike__vote=None)


def about(request):
    return HttpResponse('О проекте')

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'newstories/addpage.html'
    success_url = reverse_lazy('homepage')
    login_url = '/admin/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавить историю")
        return dict(list(context.items()) + list(c_def.items()))

def contact(request):
    return HttpResponse('Обратная связь')

def login(request):
    return HttpResponse('Авторизация')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class ShowPost(DataMixin, DetailView):
    model = Stories
    template_name = 'newstories/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'newstories/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

