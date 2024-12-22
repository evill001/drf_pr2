from django.contrib import admin
from django.urls import path, include

from api.urls import accounts_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
]

urlpatterns += accounts_urlpatterns