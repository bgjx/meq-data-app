from django import forms 

class UploadFormCatalogCSV(forms.Form):

    CATALOG_TYPE_CHOICES = [
        ('initial', 'Initial Hypocenter'),
        ('relocated', 'Relocated Hypocenter'),
        ('picking', 'Picking Catalog'),
        ('station', 'Station Data')
    ]

    catalog_type = forms.ChoiceField(
        choices=CATALOG_TYPE_CHOICES,
        widget=forms.RadioSelect
    )

    title = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Update Title'
            }
        ))
    
    file = forms.FileField()

    description = forms.CharField(
        max_length=225,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Tell us little about this update'
            }
        ))