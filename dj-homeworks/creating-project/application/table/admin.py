from django.contrib import admin

from .models import Filecsv, Fieldsfortable


class FieldsfortableAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'width')
    list_display_links = ('id', 'name')


class FilecsvAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_path')
    list_display_links = ('id', 'file_path')


admin.site.register(Filecsv, FilecsvAdmin)
admin.site.register(Fieldsfortable, FieldsfortableAdmin)
