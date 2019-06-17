from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Rubric, Relations


class RelationsInlineFormset(BaseInlineFormSet):
    def clean(self):
        primary = 0
        for form in self.forms:
            try:
                if form.cleaned_data['primary']:
                    primary += 1
            except KeyError:
                raise ValidationError('Введите рубрику для статьи!')
        if primary > 1:
            raise ValidationError('Основным может быть только один раздел')
        elif primary == 0:
            raise ValidationError('Укажите основной раздел раздел')
        return super().clean()


class RelationsInline(admin.TabularInline):
    model = Relations
    extra = 0
    formset = RelationsInlineFormset
    

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at')
    list_display_links = ('title', 'published_at')
    inlines = [RelationsInline]

@admin.register(Rubric)
class RubricAdmin(admin.ModelAdmin):
    pass
