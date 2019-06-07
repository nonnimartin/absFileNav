from django import forms

class SettingsForm(forms.Form):
    forms.CharField(label='Base Folder', max_length=4096)
    forms.BooleanField(label='Show Files')
