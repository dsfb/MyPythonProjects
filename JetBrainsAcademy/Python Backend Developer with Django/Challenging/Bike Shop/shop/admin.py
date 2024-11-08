from django.contrib import admin
from .models import Frame, Seat, Tire, Basket, Bike, Order

# Register your models here.
admin.site.register(Frame)
admin.site.register(Seat)
admin.site.register(Tire)
admin.site.register(Basket)
admin.site.register(Bike)
admin.site.register(Order)
