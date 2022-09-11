from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post, BlogComment, Tag
from django.contrib import messages
import math

# Create your views here.
def index(request):
    recent_posts = Post.objects.order_by('-createdAt').exclude(is_private=True).all()[0:2]
    context = {'recent_posts': recent_posts}
    return render(request, 'index.html', context)

def blog(request):
    allPostsCount = Post.objects.order_by('-createdAt').exclude(is_private=True).all().count()
    page = request.GET.get("page")
    no_of_posts = 5
    if not page:
        page = 1
    else:
        page = int(page)
    posts = Post.objects.order_by('-createdAt').exclude(is_private=True).all()
    length = posts.count()
    posts = posts[(page-1)*no_of_posts: page*no_of_posts]
    if page > 1:
        prev = "?page=" + str(page - 1)
    else:
        prev = None

    if page < math.ceil(length/no_of_posts):
        nxt = "?page=" + str(page + 1)
    else:
        nxt = None
    context = {'posts': posts, 'postsCount': allPostsCount, 'prev': prev, 'next': nxt}
    return render(request, "blog.html", context)

def blogpost(request, post_slug):
    post = Post.objects.filter(slug=post_slug).first()
    if post.is_private == True:
        messages.error(request, 'You cannot access private posts!')
        return redirect('/blog')
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    context = {'post': post, 'comments': comments, 'replyDict': replyDict}
    return render(request, "post.html", context)

def contact(request):
    return render(request, "contact.html")

def search(request):
    if request.GET.get("query"):
        query = request.GET.get("query")
        allPostsCount = Post.objects.filter(title__icontains=query).order_by('-createdAt').exclude(is_private=True).all().count()
        page = request.GET.get("page")
        no_of_posts = 1
        if not page:
            page = 1
        else:
            page = int(page)
        posts = Post.objects.filter(title__icontains=query).order_by('-createdAt').exclude(is_private=True).all()
        length = posts.count()
        posts = posts[(page-1)*no_of_posts: page*no_of_posts]
        if page > 1:
            prev = "?query=" + str(query) + "&page=" + str(page - 1)
        else:
            prev = None

        if page < math.ceil(length/no_of_posts):
            nxt = "?query=" + str(query) + "&page=" + str(page + 1)
        else:
            nxt = None
        context = {'posts': posts, 'postsCount': allPostsCount, 'query': query, 'prev': prev, 'next': nxt}
        return render(request, "search.html", context)
    else:
        messages.error(request, "Please provide a search query!")
        return redirect("/")

def tagged_posts(request, tag):
    post_tag = Tag.objects.filter(slug=tag).first()
    if not post_tag:
        messages.error(request, "No such tag was found against a post!")
        return redirect("/")
    allPostsCount = Post.objects.filter(tags__slug=tag).order_by('-createdAt').exclude(is_private=True).all().count()
    page = request.GET.get("page")
    no_of_posts = 5
    if not page:
        page = 1
    else:
        page = int(page)
    posts = Post.objects.filter(tags__slug=tag).order_by('-createdAt').exclude(is_private=True).all()
    length = posts.count()
    posts = posts[(page-1)*no_of_posts: page*no_of_posts]
    if page > 1:
        prev = "?page=" + str(page - 1)
    else:
        prev = None

    if page < math.ceil(length/no_of_posts):
        nxt = "?page=" + str(page + 1)
    else:
        nxt = None
    context = {'posts': posts, 'postsCount': allPostsCount, 'prev': prev, 'next': nxt, 'tag': tag}
    return render(request, "tagged_posts.html", context)