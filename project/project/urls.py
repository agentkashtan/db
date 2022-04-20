from django.contrib import admin
from django.urls import path, include

api_urls = [
    path('', include('person.urls'))
    ]

urlpatterns = [
    path('api/', include(api_urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls'))
]
