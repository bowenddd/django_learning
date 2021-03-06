from django.db import models
from django.contrib.auth.models import User
from slugify import slugify
from .fields import OrderField
# Create your models here.

class Course(models.Model):

    user = models.ForeignKey(User,models.CASCADE,related_name='course_user')

    title = models.CharField(max_length=200)

    slug = models.SlugField(max_length=200, unique=True)

    overview = models.TextField()

    student = models.ManyToManyField(User,related_name="student",blank=True)

    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ('-created',)


    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.title)
        super(Course, self).save(force_insert=force_insert,force_update=force_update,using=using,update_fields=update_fields)

    def __str__(self):
        return self.title

def user_directory_path(instance,filename):
    return 'courses/user_{}/{}'.format(instance.user.id,filename)

class Lesson(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='lesson_user')
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='lesson')
    title = models.CharField(max_length=200)
    video = models.FileField(upload_to=user_directory_path)
    description = models.TextField(blank=True)
    attach = models.FileField(upload_to=user_directory_path,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    order = OrderField(blank=True, for_fields=['course'])
    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}.{}'.format(self.order,self.title)

