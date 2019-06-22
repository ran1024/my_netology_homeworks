from django.contrib import admin

from .models import Car, Review
from .forms import ReviewAdminForm


class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'review_count')
    list_filter = ('brand',)
    list_display_links = ('brand', 'model')
    
    def review_count(self, record):
        counts = record.review_set.count()
        return f'{counts}'
        
    review_count.short_description = 'Количество статей'


class ReviewAdmin(admin.ModelAdmin):
    form = ReviewAdminForm
    list_display = ('car', 'title')
    list_display_links = ('car', 'title')
    list_filter = ('car',)
    search_fields = ('title',)


admin.site.register(Car, CarAdmin)
admin.site.register(Review, ReviewAdmin)
