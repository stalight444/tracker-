from django.urls import path
from . import views

urlpatterns = [
    path('track-visit/', views.track_visit, name='track_visit'),
    path('', views.tracker_view, name='tracker_view'),
]
