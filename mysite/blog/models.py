from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status = Post.Status.PUBLISHED)
    
class Post(models.Model):
    class Status(models.TextChoices): # https://docs.djangoproject.com/en/4.2/ref/models/fields/#choices
        DRAFT = ('DF', 'Draft')
        PUBLISHED = ('PB', 'Published')
    objects = models.Manager()
    published_manager = PublishedManager()
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='published')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices = Status.choices,
                              default = Status.DRAFT)

    class Meta:
        ordering = ['-published']
        indexes= [
            models.Index(fields= ['-published']),
        ]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.published.year,
                             self.published.month,
                             self.published.day,
                             self.slug])