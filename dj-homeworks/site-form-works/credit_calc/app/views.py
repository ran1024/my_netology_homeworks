from django.shortcuts import render

from .forms import CalcForm


def calc_view(request):
    template = "app/calc.html"

    if request.method == 'POST':
        form = CalcForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            initial_fee = form.cleaned_data['initial_fee']
            rate = form.cleaned_data['rate']
            months_count = form.cleaned_data['months_count']
            common_result = int((initial_fee + initial_fee * rate) / months_count)
            context['result'] = round(common_result / 12)
            context['common_result'] = common_result
    else:
        form = CalcForm()
        context = {'form': form}
    
    return render(request, template, context)
