from django.urls import path


from newstories.views import *

urlpatterns = [
    path('', StoriesHomepage.as_view(), name= 'homepage'),
    path('about/', about, name= 'about'),
    path('addpage/', AddPage.as_view(), name= 'add_page'),
    path('contact/', contact, name= 'contact'),
    path('login/', LoginUser.as_view(), name= 'login'),
    path('logout/', logout_user, name= 'logout'),
    path('register/', RegisterUser.as_view(), name= 'register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name= 'post'),
    path('likedislike/<slug:post_slug>/', get_like_dislike, name='likedislike'),
    path('best/', StoriesBestRating.as_view(), name='best'),
    path('worst/', StoriesWorstRating.as_view(), name='worst'),
    path('no_vote/', StoriesNoRating.as_view(), name= 'no_vote'),

]