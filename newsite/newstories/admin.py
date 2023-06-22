from django.contrib import admin

from .models import *


class StoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'get_rating','photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('title','time_create', 'is_published')

    def get_rating(self, obj):
        return obj.get_rating()
    get_rating.short_description = 'Рейтинг'





class LikedislikeAdmin(admin.ModelAdmin):
    list_display = ('vote', 'get_story')
    list_display_links = ('vote',  )
    search_fields = ('id',)

    def get_story(self, obj):
        return obj.story
    get_story.short_description = 'История'

admin.site.register(Stories, StoriesAdmin)
admin.site.register(LikeDislike, LikedislikeAdmin)

