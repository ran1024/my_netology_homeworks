from collections import Counter

from django.shortcuts import render_to_response

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    ind = request.GET.get('from-landing')
    counter_show[ind] += 1
    return render_to_response('index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    ind = request.GET.get('ab-test-arg')
    counter_click[ind] += 1
    if ind == 'original':
        return render_to_response('landing.html')
    return render_to_response('landing_alternate.html')


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Чтобы отличить с какой версии лендинга был переход
    # проверяйте GET параметр marker который может принимать значения test и original
    # Для вывода результат передайте в следующем формате:
    context_dict = {
        'test_conversion': 0.5,
        'original_conversion': 0.4,
    }
    for i in context_dict:
        ind, _ = i.split('_')
        context_dict[i] = counter_show[ind] / counter_click[ind] if counter_click[ind] else 0

    return render_to_response('stats.html', context=context_dict)
