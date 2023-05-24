from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
import json
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView
)
from .models import *
from .forms import *

def home(request):
    context = {
        'bookings': Booking.objects.all()
    }
    return render(request, 'booking/home.html', context)


class BookingListView(ListView):
    model = Booking
    template_name = 'booking/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'bookings'
    ordering = ['date']
    paginate_by = 10

class BookingDetailView(DetailView):
    model = Booking

class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingCreateForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BookingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Booking
    success_url = '/'

    def test_func(self):
        booking = self.get_object()
        if self.request.user == booking.user:
            return True
        return False

def about(request):
    return render(request, 'booking/about.html', {'title': 'About'})

@login_required
def get_choices(request):
    if request.method == 'POST':
        try:
            parent_id = request.POST.get('parent_id')
            element_id = request.POST.get('element_id')
            objects = None
            image = None
            if element_id == 'id_department':
                image = Building.objects.get(id=parent_id).image
                objects = Department.objects.filter(building=parent_id)
            elif element_id == 'id_room':
                image = Department.objects.get(id=parent_id).image
                objects = Room.objects.filter(department=parent_id)
            elif element_id == 'id_desk':
                image = Room.objects.get(id=parent_id).image
                objects = Desk.objects.filter(room=parent_id)
            else:
                objects = Building.objects.all()

            data = {
                'image_url': '' if image == None else image.url,
                'choices': {
                    obj.id: {
                        'name': obj.name,
                        'shape': '' if obj.map == None else obj.map.shape,
                        'coords': '' if obj.map == None else obj.map.coords
                    } for obj in objects.order_by('name')
                }
            }
            return JsonResponse(json.dumps(data), safe=False)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    return JsonResponse(json.dumps({}), safe=False)

