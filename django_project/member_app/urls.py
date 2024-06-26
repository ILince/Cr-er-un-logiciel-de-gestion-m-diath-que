from django.urls import path

from . import views

urlpatterns = [
    path('menu/', views.list_all_media, name='member_menu'),
]
