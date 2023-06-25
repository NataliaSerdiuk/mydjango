from django.urls import path


from newstories.views import *

urlpatterns = [
    path('', index, name= 'homepage'),
    path('about/', about, name= 'about'),
    path('addpage/', addpage, name= 'add_page'),
    path('contact/', contact, name= 'contact'),
    path('login/', login, name= 'login'),
    path('post/<slug:post_slug>/', show_post, name= 'post'),
    path('best/', best_view, name='best'),
    path('worst/', worst_view, name='worst'),
    path('no_vote', no_vote, name= 'no_vote'),

]