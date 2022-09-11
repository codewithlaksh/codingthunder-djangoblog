from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils.text import slugify

# Create your models here.
class Tag(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, null=True, blank=True)
    updatedAt = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=800)
    slug = models.SlugField(max_length=800, null=True, blank=True)
    tagline = models.CharField(max_length=800)
    tags = models.ManyToManyField(Tag)
    is_private = models.BooleanField(default=False, verbose_name='Private Post')
    description = models.TextField()
    updatedAt = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    comment = models.CharField(max_length=12000)
    createdAt = models.DateTimeField(auto_now_add=True)

class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    message = models.TextField()
    createdAt = models.DateTimeField(default=now)
