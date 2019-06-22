from django import forms

from .widgets import AjaxInputWidget
from .models import City


class SearchTicket(forms.Form):
    # Добавьте здесь поля, описанные в задании
    city_out = forms.CharField(label='Город отправления',
                               widget=AjaxInputWidget('api/city_ajax', attrs={'class':'inline right-margin'}))
    city_in = forms.ModelChoiceField(queryset=City.objects.order_by('name'), label='Город прибытия',
                                     widget=forms.widgets.Select(attrs={'style':'padding:3px;margin:0 20px 0 0'}))
    data = forms.DateField(label='Дата', widget=forms.widgets.SelectDateWidget())

