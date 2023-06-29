from .models import *


menu = [ {'title': "О сайте", 'url_name': 'about'},
         {'title':" Добавить историю", 'url_name': 'add_page'},
         {'title':"Обратная связь",'url_name': 'contact'},
         {'title':"Войти на сайт", 'url_name': 'login'},
         {'vote_selected': 0, 'url_name': 'no_vote'},
         {'vote_selected': 1, 'url_name': 'best'},
         {'posts_selected': 0, 'url_name': 'homepage'},
]


class DataMixin:
    paginate_by = 3
    def get_user_context(self, **kwargs):
        context = kwargs
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)
        context['menu'] = user_menu
        return context