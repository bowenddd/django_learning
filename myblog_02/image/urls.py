from django.urls import path
from . import views
urlpatterns = [
    path('list-images/',views.list_image,name="list_image"),
    path('upload-image/',views.upload_image,name="upload_image"),
    path('delete-image/',views.del_image,name='del_image'),
    path('falls-images/',views.falls_images,name='falls_images')
]