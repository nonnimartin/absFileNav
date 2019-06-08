from django import forms

class SettingsForm(forms.ModelForm):
    forms.CharField(label='Base Folder', max_length=4096)
    forms.BooleanField(label='Show Files')