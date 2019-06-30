from django.contrib import admin

from .models import Station, Route


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    pass


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude')
    list_display_links = ('name', 'latitude', 'longitude')
    search_fields = ('name',)
    filter_horizontal = ('routes',)
