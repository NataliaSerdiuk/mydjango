from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound

from .forms import *
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

def no_vote(request):
    # Получаем список неоцененных историй
    no_vote_stories = Stories.objects.filter(likedislike__vote=None)

    context = {
        'posts': no_vote_stories,
        'menu': menu,
        'title': 'Неоцененные истории',
        'vote_selected': 0
    }
    return render(request, 'newstories/no_vote.html', context=context)


def about(request):
    return HttpResponse('О проекте')

def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            # user_text = form.cleaned_data['content']
            # user_text_list = user_text.split()
            # with open('D:/Python/djangosite/newsite/newstories/resources/forbidden_words.txt', 'r') as file:
            #     forbidden_words = [word.strip() for word in file.readlines()]
            #     for word in forbidden_words:
            #         if word in user_text_list:
            #             raise ValidationError("Текст содержит недопустимое слово.")
            #         else:
            form.save()
            return redirect('no_vote')
    else:
        form = AddPostForm()
    return render(request, 'newstories/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавь свою историю'})

def contact(request):
    return HttpResponse('Обратная связь')

def login(request):
    return HttpResponse('Авторизация')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def show_post(request, post_slug):
    post = get_object_or_404(Stories, slug=post_slug)

    context = {
        'post' : post,
        'menu': menu,
        'title': post.title,
        'posts_selected': 0
    }

    return render(request, 'newstories/post.html', context=context)


