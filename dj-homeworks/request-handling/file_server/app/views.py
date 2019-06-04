import os
from datetime import datetime

from django.shortcuts import render
from django.conf import settings


def file_list(request, year=None, month=None, day=None):
    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
    template_name = 'index.html'
    context = {'files': [], 'date': None}
    arr = os.listdir(settings.FILES_PATH)
    arr.sort()
    if year:
        context['date'] = datetime(year, month, day).date()
    for fl in arr:
        stat_info = os.stat(f'{settings.FILES_PATH}/{fl}')
        ctime = datetime.fromtimestamp(stat_info.st_ctime).date()
        if context['date'] == ctime or not year:
            context['files'].append({'name': fl,
                'ctime': ctime,
                'mtime': datetime.fromtimestamp(stat_info.st_mtime).date(),
            })      

    return render(request, template_name, context)


def file_content(request, name):
    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
    context={'file_name': name, 'file_content': ''}
    with open(settings.FILES_PATH + '/' + name) as fh:
        context['file_content'] = fh.read()
    
    return render(request, 'file_content.html', context)

