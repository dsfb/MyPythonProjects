from django.urls import path

from . import views

urlpatterns = [
    path("bikes/", views.bikes, name="bikes"),
    path('bikes/<int:pk>/', views.BikeView.as_view(), name='bike_detail'),
path('order/<int:pk>/', views.OrderView.as_view(), name='order'),
]
