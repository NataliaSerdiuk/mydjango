from django.db import models

from django.db.models import Sum
from django.urls import reverse


class Stories(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    content = models.TextField(blank=True, verbose_name='Содержание')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/",blank=True, verbose_name='Фотография')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})

    def get_rating(self):
        return self.likedislike_set.aggregate(rating=Sum('vote'))['rating'] or 0


    class Meta:
        verbose_name = 'Выдуманные истории'
        verbose_name_plural = 'Выдуманные истории'
        ordering = ['time_create', 'title']


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1
    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )
    vote = models.SmallIntegerField(default=0, verbose_name="Голос", choices=VOTES)
    story = models.ForeignKey(Stories, verbose_name="История", on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Лайк/дислайк'
        verbose_name_plural = 'Лайк/дислайк'



    def get_absolute_url(self):
        return reverse('likedislike', kwargs={'vote_id': self.pk})


    def get_story(self, obj):
        return obj.story







