from django.views.generic import ListView
from django.shortcuts import render
from django.db.models import Prefetch

from articles.models import Article, Rubric, Relations


def articles_list(request):
    template = 'articles/news.html'
    pr1 = Prefetch('rubrics', queryset=Relations.objects.select_related('rubric').order_by('-primary', 'rubric'))
    object_list = Article.objects.prefetch_related(pr1).order_by('-published_at')
    context = {'object_list': object_list}

    return render(request, template, context)
