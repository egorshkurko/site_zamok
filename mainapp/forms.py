from django import forms

class OrderForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ваше имя',
            'required': True
        })
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '+7 (___)-___-__-__',
            'required': True
        })
    )
    service_type = forms.ChoiceField(
        choices=[
            ('unlock', 'Вскрытие дверей'),
            ('replace', 'Замена замков'),
            ('repair', 'Ремонт замков'),
            ('other', 'Другая услуга')
        ],
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )