from django import forms

class CSVForm(forms.Form):
    csv = forms.FileField(
        label='Upload CSV File of Game Reviews',
        widget=forms.ClearableFileInput(attrs={'accept': '.csv'}),
    )
