from django.urls import path

from . import views


urlpatterns = [
    path('', views.LinkListView.as_view(), name='links'),
]
