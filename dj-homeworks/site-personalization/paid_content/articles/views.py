from django.shortcuts import render
from .models import Article, AdvUser


def show_articles(request):
    articles = Article.objects.all()
    context = {'articles_list': articles}
    return render(request, 'articles.html', context)


def show_article(request, id):
    visible = False
    is_login = True
    article = Article.objects.get(pk=id)
    
    if request.method == 'POST':
        if not request.user.is_anonymous:
            a = AdvUser.objects.get(pk=request.user.id)
            a.is_subscribe = True
            a.save()
    else:
        if request.user.is_anonymous:
            print(request.user)
            article.body = 'Для того, чтобы читать данную статью, необходимо авторизоваться' \
                           ' на сайте и подписаться на журнал.'
            visible = True
            is_login = False
        elif article.is_paid and not request.user.is_subscribe:
            article.body = 'Для того, чтобы читать данную статью, необходимо подписаться на журнал.'
            visible = True
    context = {'article': article, 'visible': visible, 'is_login': is_login}
    return render(request, 'article.html', context )
