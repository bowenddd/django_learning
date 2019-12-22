from django.db import models
from django.contrib.auth.models import User
from slugify import slugify

# Create your models here.

class Image(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='images')

    title = models.CharField(max_length=300)

    slug = models.SlugField(max_length=500,blank=True)

    url = models.URLField()

    description = models.TextField(blank=True)

    created = models.DateField(auto_now_add=True,db_index=True)

    image = models.ImageField(upload_to='images/%Y/%m/%d')

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.title)
        super(Image, self).save(force_insert=force_insert,force_update=force_update,using=using,
                                update_fields=update_fields)
