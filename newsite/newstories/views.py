from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.db.models import Sum

from .models import *


menu = [ {'title': "О сайте", 'url_name': 'about'},
         {'title':" Добавить историю", 'url_name': 'add_page'},
         {'title':"Обратная связь",'url_name': 'contact'},
         {'title':"Войти на сайт", 'url_name': 'login'},
]

like_dislike = [ {'title': "Лучшие истории", 'url_name': 'best'},
                 {'title': "Скучные истории", 'url_name': 'worst'}

]
def index(request):
    posts = Stories.objects.all()

    context = {
        'posts': posts,
        'menu': menu,
        'title': 'Главная страница',
        'posts_selected' : 0
    }
    return render(request, 'newstories/index.html', context=context)



def best_view(request):
    # Получаем список лучших историй
    best_stories = Stories.objects.annotate(rating=Sum('likedislike__vote')).order_by('-rating').filter(rating__gt=0)

    context = {
        'posts': best_stories,
        'menu': menu,
        'title': 'Лучшие истории',
        'vote_selected': 1
    }
    return render(request, 'newstories/best.html', context=context)

def worst_view(request):
    # Получаем список скучных историй (рейтинг 0)
    worst_stories = Stories.objects.annotate(rating=Sum('likedislike__vote')).order_by('-rating').filter(rating__lt=1)

    context = {
        'posts': worst_stories,
        'menu': menu,
        'title': 'Скучные истории',
        'vote_selected': -1
    }
    return render(request, 'newstories/worst.html', context=context)


def about(request):
    return HttpResponse('О проекте')

def addpage(request):
    return HttpResponse('Добавить историю')

def contact(request):
    return HttpResponse('Обратная связь')

def login(request):
    return HttpResponse('Авторизация')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def show_post(request,post_id):
    return HttpResponse(f"Отображение статьи с id = {post_id}")