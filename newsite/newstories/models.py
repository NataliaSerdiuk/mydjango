from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse



class Stories(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название истории')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(blank=True, verbose_name='Текст истории')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/",blank=True, verbose_name='Фото')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовать')
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

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
    vote = models.SmallIntegerField(verbose_name="Голос", choices=VOTES)
    story = models.ForeignKey(Stories, verbose_name="История", on_delete=models.PROTECT)
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)


    class Meta:
        verbose_name = 'Лайк/дислайк'
        verbose_name_plural = 'Лайк/дислайк'


    def get_absolute_url(self):
        return reverse('likedislike', kwargs={'vote_id': self.pk})

    @property
    def get_story(self):
        return self.story