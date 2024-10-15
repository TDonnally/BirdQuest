from django import forms

class BirdImageUploadForm(forms.Form):
    image = forms.ImageField(
        required=True, 
        widget=forms.FileInput(attrs={'id': 'file-upload', 'style': 'display:none'})
    )

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.content_type not in ['image/jpeg', 'image/png']:
                raise forms.ValidationError("Only JPEG and PNG files are supported.")
        return image