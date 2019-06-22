from django import forms


class CalcForm(forms.Form):
    initial_fee = forms.IntegerField(label="Стоимость товара")
    rate = forms.IntegerField(label="Процентная ставка", initial=0, min_value=0, max_value=100)
    months_count = forms.IntegerField(label="Срок кредита в месяцах", initial=0, min_value=0, max_value=12)

    def clean_initial_fee(self):
        # валидация одного поля, функция начинающаяся на `clean_` + имя поля
        initial_fee = self.cleaned_data.get('initial_fee')
        if initial_fee < 0:
            raise forms.ValidationError("Стоимость товара не может быть отрицательной")
        elif initial_fee == 0:
            raise forms.ValidationError("Бесплатный сыр бывает только в мышеловке!")
        return initial_fee

    def clean_rate(self):
        rate = self.cleaned_data.get('rate')
        if rate > 90:
            raise forms.ValidationError("Ну это уже вообще грабёж!")
        return rate

    def clean(self):
        # общая функция валидации
        if self.cleaned_data['months_count'] == 0:
            self.cleaned_data['months_count'] = 1  # иначе будет деление на 0.
        
        return self.cleaned_data
