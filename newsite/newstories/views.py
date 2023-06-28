from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy

from .forms import *
from .models import *


menu = [ {'title': "О сайте", 'url_name': 'about'},
         {'title':" Добавить историю", 'url_name': 'add_page'},
         {'title':"Обратная связь",'url_name': 'contact'},
         {'title':"Войти на сайт", 'url_name': 'login'},
]

class StoriesHomepage(ListView):
    model = Stories
    template_name = 'newstories/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return Stories.objects.filter(is_published = True)

class StoriesBestRating(ListView):
    model = LikeDislike
    template_name = 'newstories/best.html'
    context_object_name = 'posts'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Лучшие истории'
        context['vote_selected'] = 1
        return context
    def get_queryset(self):
        return Stories.objects.annotate(rating=Sum('likedislike__vote')).order_by('-rating').filter(rating__gt=0)

class StoriesWorstRating(ListView):
    model = LikeDislike
    template_name = 'newstories/worst.html'
    context_object_name = 'posts'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Скучные истории'
        context['vote_selected'] = -1
        return context
    def get_queryset(self):
        return Stories.objects.annotate(rating=Sum('likedislike__vote')).order_by('-rating').filter(rating__lt=1)

class StoriesNoRating(ListView):
    model = LikeDislike
    template_name = 'newstories/no_vote.html'
    context_object_name = 'posts'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Неоцененные истории'
        context['vote_selected'] = 0
        return context
    def get_queryset(self):
        return Stories.objects.filter(likedislike__vote=None)


def about(request):
    return HttpResponse('О проекте')

class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'newstories/addpage.html'
    success_url = reverse_lazy('homepage')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Добавить историю'
        return context

def contact(request):
    return HttpResponse('Обратная связь')

def login(request):
    return HttpResponse('Авторизация')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class ShowPost(DetailView):
    model = Stories
    template_name = 'newstories/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = context['post']
        return context



