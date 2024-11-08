from idlelib.debugger_r import frametable

from django.http import HttpResponse
from django.shortcuts import  redirect, render
from django.template import loader
from django.views import View

from .forms import BikeOrderingForm
from .models import Basket, Bike, Order

# Create your views here.
def bikes(request):
    available_bike_list = Bike.objects.all()
    template = loader.get_template("bikes.html")
    context = {
        "available_bikes": available_bike_list,
    }
    return HttpResponse(template.render(context, request))

class BikeView(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        bike = Bike.objects.filter(id=pk).first()

        bike_available = bike.frame.quantity > 0 and \
                         bike.tire.quantity >= 2 and \
                         bike.seat.quantity > 0

        form = BikeOrderingForm()

        return render(request, 'bikedetails.html',
                      {'bike': bike, 'form': form,
                       'bike_available': bike_available})

    def post(self, request, *args, **kwargs):
        data = request.POST
        form = BikeOrderingForm(data)
        pk = self.kwargs['pk']
        bike = Bike.objects.filter(id=pk).first()

        if form.is_valid():
            new_order = Order()
            new_order.bike = bike
            new_order.name = form.fields['name']
            new_order.surname = form.fields['surname']
            new_order.phone_number = form.fields['phone_number']
            new_order.status = 'P'
            new_order.save()

            frame = bike.frame
            frame.quantity -= 1
            frame.save()

            tire = bike.tire
            tire.quantity -= 2
            tire.save()

            seat = bike.seat
            seat.quantity -= 1
            seat.save()

            if bike.has_basket:
                basket = Basket.objects.first()
                basket.quantity -= 1
                basket.save()

            return redirect('order', pk=new_order.pk)

        return redirect('.')


class OrderView(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        return render(request, 'order.html',
                      {'order_number': pk, })
