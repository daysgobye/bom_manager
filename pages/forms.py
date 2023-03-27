from django import forms

class csv_upload(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)