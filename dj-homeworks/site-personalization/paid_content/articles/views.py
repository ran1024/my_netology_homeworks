from django.shortcuts import render
from .models import Article, AdvUser


def show_articles(request):
    articles = Article.objects.all()
    context = {'articles_list': articles}
    return render(request, 'articles.html', context)


def show_article(request, id):
    visible = False
    article = Article.objects.get(pk=id)
    
    if request.method == 'POST':
        a = AdvUser.objects.get(pk=request.user.id)
        a.is_subscribe = True
        a.save()
    else:
        if article.is_paid and not request.user.is_subscribe:
            article.body = 'Для того, чтобы читать данную статью, необходимо подписаться на журнал.'
            visible = True
    context = {'article': article, 'visible': visible}
    return render(request, 'article.html', context )
