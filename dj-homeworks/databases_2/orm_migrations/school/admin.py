from django.contrib import admin

from .models import Student, Teacher


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'group')
    list_display_link = ('name', 'group')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass
