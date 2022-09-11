from django.contrib import admin

from home.models import BlogComment, Contact, Post, Tag

# Register your models here.
admin.site.register((Tag, BlogComment, Contact))

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Media:
        js= ('tinyMCE.js',)