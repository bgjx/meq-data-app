from django import forms 

class UploadFormCatalogCSV(forms.Form):

    title = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Update Title'
            }
        ))
    
    file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'placeholder': 'Drop your file here'
            }
        )
    )
    
    description = forms.CharField(
        max_length=225,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Tell us little about this update'
            }
        ))