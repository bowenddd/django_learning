from django.urls import path
from . import views

urlpatterns = [
    path('',views.show_title),
    path('<int:article_id>/',views.show_content),
]