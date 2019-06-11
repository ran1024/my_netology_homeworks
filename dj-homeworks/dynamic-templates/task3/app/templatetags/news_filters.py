from django import template
import time

register = template.Library()

current_time = time.time()

@register.filter
def format_date(value):
    delta = current_time - value
    if delta < 60*10:
        return 'только что'
    elif delta < 60*60:
        return f'{int(delta // 60)} минут назад'
    elif delta < 60*24*10:
        return f'{int(delta // 3600)} часов назад'
    else:
        d = time.localtime(value)
        return f'{d.tm_year}-{d.tm_mon}-{d.tm_mday}'

@register.filter
def format_scope(value):
    if value < -5:
        return 'всё плохо'
    elif -5 <= value <= 5:
        return 'нейтрально'
    else:
        return 'хорошо' 

@register.filter
def format_num_comments(value):
    if value == 0:
        return 'Оставьте комментарий'
    elif 0 < value <= 50:
        return value
    else:
        return '50+'

@register.filter
def format_selftext(value):
    text_list = value.split(' ')
    value = ' '.join(text_list[:5]) + ' . . . ' + ' '.join(text_list[-5:])
    return value


