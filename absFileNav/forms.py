from django import forms

class FileUploadPath(forms.Form):
    path = forms.CharField(label='Where do you want to save the file?', max_length=255)