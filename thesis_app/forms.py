from django import forms
from django.core.exceptions import ValidationError

class CSVForm(forms.Form):
    csv = forms.FileField(
        label='Upload CSV File of Game Reviews',
        widget=forms.ClearableFileInput(attrs={'accept': '.csv'}),
    )

    model_choices = [('opt_with', 'With Emojis and Emoticons'), ('opt_without', 'Without Emojis and Emoticons')]
    model_field = forms.ChoiceField(
        choices=model_choices,
        widget=forms.RadioSelect,
        label='Select the Model for analyzing the file',
        initial='opt_with',
    )