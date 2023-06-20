from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Sum
from django.urls import reverse


class Stories(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    content = models.TextField(blank=True, verbose_name='Содержание')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/",blank=True, verbose_name='Фотография')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    # cat = models.ForeignKey('Categories', on_delete=models.PROTECT, null=True, verbose_name='Категории')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})

# class LikeDislikeManager(models.Manager):
#     use_for_related_fields = True
#
#     def likes(self):
#         # Забираем queryset с записями больше 0
#         return self.get_queryset().filter(vote__gt=0)
#
#     def dislikes(self):
#         # Забираем queryset с записями меньше 0
#         return self.get_queryset().filter(vote__lt=0)
#
#     def sum_rating(self):
#         # Забираем суммарный рейтинг
#         return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1
    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )
    vote = models.SmallIntegerField(verbose_name="Голос", choices=VOTES)
    story = models.ForeignKey(Stories, verbose_name="История", on_delete=models.PROTECT)

    # objects = LikeDislikeManager()


    def get_absolute_url(self):
        return reverse('likedislike', kwargs={'vote_id': self.pk})





