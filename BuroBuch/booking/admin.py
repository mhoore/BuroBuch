from django.contrib import admin
from .models import *

admin.site.register(Building)
admin.site.register(Department)
admin.site.register(Room)
admin.site.register(Desk)
admin.site.register(Booking)