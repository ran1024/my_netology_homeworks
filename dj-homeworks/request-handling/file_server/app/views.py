import os
from datetime import datetime
from django.shortcuts import render
from django.conf import settings


def file_list(request, date=None):
    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
    template_name = 'index.html'
    context = {'files': [], 'date': date}
    arr = os.listdir(settings.FILES_PATH)
    arr.sort()
    if date:
        dd = [int(x) for x in date.split('-')]
        context['date'] = datetime(*dd).date()
    for fl in arr:
        stat_info = os.stat(f'{settings.FILES_PATH}/{fl}')
        c_time = datetime.fromtimestamp(stat_info.st_ctime)
        m_time = datetime.fromtimestamp(stat_info.st_mtime)
        if context['date'] == c_time.date() or context['date'] == m_time.date() or not date:
            context['files'].append({
                'name': fl,
                'ctime': c_time,
                'mtime': m_time,
            })      
    return render(request, template_name, context)


def file_content(request, name):
    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
    context = {'file_name': name, 'file_content': ''}
    with open(settings.FILES_PATH + '/' + name) as fh:
        context['file_content'] = fh.read()
    
    return render(request, 'file_content.html', context)

