from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('characters/', include('characters.urls')),
    path('admin/', admin.site.urls)
]
