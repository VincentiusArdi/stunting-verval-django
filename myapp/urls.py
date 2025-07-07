from django.urls import path
from .views import (
    getDataVervalByLocationWithPagination)

urlpatterns = [
    path('getDataVervalByLocationWithPagination', getDataVervalByLocationWithPagination, name='getDataVervalByLocationWithPagination'),
]