from django import forms


class SettingsForm(forms.Form):
    base_folder = forms.CharField(label='Base Folder', max_length=4096)
    #show_files  = forms.BooleanField(label='Show Files', required=False)
