from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UpdateDataViewSet

router = DefaultRouter()
router.register(r'data', UpdateDataViewSet, basename='data')

app_name = 'person'
urlpatterns = [
    path('', include(router.urls)),
]
