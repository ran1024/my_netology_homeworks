from django.contrib import admin
from .models import Phone


class PhoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'release_date', 'lte_exists')
    list_display_links = ('id', 'name')
    

admin.site.register(Phone, PhoneAdmin)
