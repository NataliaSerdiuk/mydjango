from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login


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

def get_like_dislike(request, post_slug):
    post = get_object_or_404(Stories, slug=post_slug)
    existing_vote = None

    if request.method == 'POST' and request.user.is_authenticated:
        vote = request.POST.get('vote')
        existing_vote = LikeDislike.objects.filter(story=post, author=request.user).first()

        if not existing_vote:
            if vote == 'like':
                LikeDislike.objects.create(vote=LikeDislike.LIKE, story=post, author=request.user)
            elif vote == 'dislike':
                LikeDislike.objects.create(vote=LikeDislike.DISLIKE, story=post, author=request.user)
            return redirect('post', post_slug=post.slug)
        if existing_vote.vote == 1:
            if vote == 'dislike':
                existing_vote.delete()
                LikeDislike.objects.create(vote=LikeDislike.DISLIKE, story=post, author=request.user)
            return redirect('post', post_slug=post.slug)
        if existing_vote.vote == -1:
            if vote == 'like':
                existing_vote.delete()
                LikeDislike.objects.create(vote=LikeDislike.LIKE, story=post, author=request.user)
            return redirect('post', post_slug=post.slug)

    context = {
        'post': post,
        'existing_vote': existing_vote,
    }
    return render(request, 'newstories/post.html', context)

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

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'newstories/contact.html'
    success_url = reverse_lazy('homepage')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        return redirect('homepage')

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

        rating = self.object.get_rating()
        context['rating'] = rating

        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'newstories/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('homepage')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'newstories/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('homepage')

def logout_user(request):
    logout(request)
    return redirect('login')