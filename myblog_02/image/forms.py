from django import forms
from slugify import slugify
from urllib import request
from django.core.files.base import ContentFile
from .models import Image

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title','description','url')

    def clean_url(self):
        url = self.cleaned_data['url']
        vaild_extensions = ['jpg', ' jpeg', 'png']

        extension = url.rsplit('.',1)[1].lower()

        if extension not in vaild_extensions:
            raise forms.ValidationError('The given url not match vaild image extension.')
        return url

    def save(self, commit=True):
        image = super(ImageForm,self).save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = '{}.{}'.format(slugify(image.title),image_url.rsplit('.',1)[1].lower())
        response = request.urlopen(image_url)
        image.image.save(image_name,ContentFile(response.read()),save=False)

        if commit:
            image.save()

        return image