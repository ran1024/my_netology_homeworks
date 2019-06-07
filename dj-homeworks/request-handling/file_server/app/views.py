import os
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.conf import settings


def file_list(request, date=None):
    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
    template_name = 'index.html'
    context = {'files': [], 'date': date}
    arr = os.listdir(settings.FILES_PATH)
    arr.sort()
    if date and '-' in date:
        dd = datetime.strptime(date, '%Y-%m-%d')
        context['date'] = dd.date()
    for fl in arr:
        stat_info = os.stat(os.path.join(settings.FILES_PATH, fl))
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
    file_path = os.path.join(settings.FILES_PATH, name)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path) as fh:
            context['file_content'] = fh.read()
    else:
        return HttpResponseNotFound(f'<h2>File {file_path} not found!</h2>')
    return render(request, 'file_content.html', context)

