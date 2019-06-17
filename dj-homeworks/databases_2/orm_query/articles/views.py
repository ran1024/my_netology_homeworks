from django.views.generic import ListView
from django.shortcuts import render
from django.db.models import Prefetch

from .models import Article, Author, Genre


def articles_list(request):
    template_name = 'articles/news.html'
    pr1 = Prefetch('author', queryset=Author.objects.only('name').all())
    pr2 = Prefetch('genre', queryset=Genre.objects.only('name').all())
    object_list = Article.objects.prefetch_related(pr1, pr2).defer('published_at', 'image').order_by('-published_at')
    context = {'object_list': object_list}

    return render(request, template_name, context)
