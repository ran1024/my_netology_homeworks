from django.contrib import admin
from .models import Manufacturer, Phone, Samsung, Xiaomi, Asus


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    pass
    

@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ('vendorname', 'model', 'price', 'os', 'typesim')
    list_display_links = ('vendorname', 'model', 'price')


@admin.register(Asus)
class AsusAdmin(admin.ModelAdmin):
    pass
    
    
@admin.register(Samsung)
class SamsungAdmin(admin.ModelAdmin):
    pass


@admin.register(Xiaomi)
class XiaomiAdmin(admin.ModelAdmin):
    pass

