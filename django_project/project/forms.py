from django import forms 

class UploadFormCatalogCSV(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
    description = forms.CharField(max_length=225)