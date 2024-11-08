from django.db import models

# write your models here
class Frame(models.Model):
    color = models.CharField(max_length=64)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return "{} frame(s) of color {}".format(self.quantity,
            self.color)


class Seat(models.Model):
    color = models.CharField(max_length=64)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return "{} seats of color {}".format(self.quantity,
            self.color)


class Tire(models.Model):
    type = models.CharField(max_length=128)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return "{} tires of type {}".format(self.quantity,
            self.type)


class Basket(models.Model):
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return "{} baskets".format(self.quantity)

class Bike(models.Model):
    frame = models.ForeignKey(Frame, on_delete=models.CASCADE)
    tire = models.ForeignKey(Tire, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, default="")
    description = models.TextField(default="")
    has_basket = models.BooleanField(default=False)

    def __str__(self):
        return "Bike: {}".format(self.name)

class Order(models.Model):
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=32)
    status = models.CharField(max_length=1)

    def __str__(self):
        return "Order: {}, with status: {}".format(self.name,
            self.status)