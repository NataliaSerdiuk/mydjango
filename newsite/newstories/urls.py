from django.urls import path


from newstories.views import *

urlpatterns = [
    path('', StoriesHomepage.as_view(), name= 'homepage'),
    path('about/', about, name= 'about'),
    path('addpage/', AddPage.as_view(), name= 'add_page'),
    path('contact/', contact, name= 'contact'),
    path('login/', login, name= 'login'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name= 'post'),
    path('best/', StoriesBestRating.as_view(), name='best'),
    path('worst/', StoriesWorstRating.as_view(), name='worst'),
    path('no_vote/', StoriesNoRating.as_view(), name= 'no_vote'),

]