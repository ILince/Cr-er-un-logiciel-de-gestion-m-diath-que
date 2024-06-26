from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('librarian_app/', include('librarian_app.urls')),
    path('member_app/', include('member_app.urls')),
]
