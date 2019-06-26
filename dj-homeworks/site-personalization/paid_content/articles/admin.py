from django.contrib import admin
from .models import AdvUser, Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_paid')
    list_filter = ('is_paid',)
    search_fields = ('title',)
    

admin.site.register(AdvUser)
admin.site.register(Article, ArticleAdmin)
