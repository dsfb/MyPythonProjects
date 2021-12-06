from collections import deque
from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import redirect, render


oil_service_number = 0
tires_service_number = 0
diagnostic_service_number = 0
oil_time_waiter = 0
tires_time_waiter = 0
diagnostic_time_waiter = 0
oil_queue = deque()
tires_queue = deque()
diagnostic_queue = deque()
current_customer_ticket = 1
next_customer_dict = {
    'oil': deque(),
    'tires': deque(),
    'diagnostic': deque()
}
next_ticket = None
last_processed = None


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "menu.html")


class OilView(View):
    def get(self, request, *args, **kwargs):
        global current_customer_ticket
        global oil_service_number
        global oil_time_waiter
        oil_service_number += 1
        oil_queue.append(oil_service_number)
        data = {
            'time': oil_time_waiter,
            'service': oil_service_number
        }
        oil_time_waiter += 2
        next_customer_dict['oil'].append(current_customer_ticket)
        current_customer_ticket += 1
        return render(request, "oil.html", data)


class TireView(View):
    def get(self, request, *args, **kwargs):
        global current_customer_ticket
        global tires_service_number
        global tires_time_waiter
        tires_service_number += 1
        tires_queue.append(tires_service_number)
        data = {
            'time': tires_time_waiter + oil_time_waiter,
            'service': tires_service_number
        }
        tires_time_waiter += 5
        next_customer_dict['tires'].append(current_customer_ticket)
        current_customer_ticket += 1
        return render(request, "tires.html", data)


class DiagnosticView(View):
    def get(self, request, *args, **kwargs):
        global current_customer_ticket
        global diagnostic_service_number
        global diagnostic_time_waiter
        diagnostic_service_number += 1
        diagnostic_queue.append(diagnostic_service_number)
        data = {
            'time': diagnostic_time_waiter + tires_time_waiter + oil_time_waiter,
            'service': diagnostic_service_number
        }
        diagnostic_time_waiter += 30
        next_customer_dict['diagnostic'].append(current_customer_ticket)
        current_customer_ticket += 1
        return render(request, "diagnostic.html", data)


class ProcessingView(View):
    def get(self, request, *args, **kwargs):
        data = {
            'oil': oil_service_number,
            'tires': tires_service_number,
            'diagnostic': diagnostic_service_number
        }
        return render(request, "processing.html", data)

    def post(self, request, *args, **kwargs):
        global last_processed
        global next_customer_dict
        global next_ticket

        global oil_time_waiter
        global tires_time_waiter
        global diagnostic_time_waiter
        if len(oil_queue):
            next_ticket = next_customer_dict['oil'].popleft()
            last_processed = oil_queue.popleft()
            oil_time_waiter -= 2
        elif len(tires_queue):
            next_ticket = next_customer_dict['tires'].popleft()
            last_processed = tires_queue.popleft()
            tires_time_waiter -= 5
        elif len(diagnostic_queue):
            next_ticket = next_customer_dict['diagnostic'].popleft()
            last_processed = diagnostic_queue.popleft()
            diagnostic_time_waiter -= 30
        else:
            last_processed = None

        return redirect('next/')


class NextView(View):
    def get(self, request, *args, **kwargs):
        data = {
            'available': last_processed is not None,
            'ticket': next_ticket
        }

        return render(request, "next.html", data)