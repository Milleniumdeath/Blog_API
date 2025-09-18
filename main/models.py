from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import  gettext_lazy as _

class PublishedManager(models.Manager):
    def get_queryset(self):
        super().get_queryset().filter(published=True)


class Article(models.Model):
    title = models.CharField(verbose_name=_('title'), max_length=255)
    cover = models.ImageField(_('cover'), upload_to='articles/', blank=True, null=True)
    context = models.TextField(_('context'))
    published = models.BooleanField(_('published'),default=False)
    created_at = models.DateTimeField(_('created_at'),auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('author'))
    views = models.PositiveSmallIntegerField(default=0)

    objects = models.Manager()
    publisheds  = PublishedManager()

    class Meta:
        verbose_name = _('article'),
        verbose_name_plural = _('articles'),
    def __str__(self):
        return f"{self.author.username} | {self.title}"

