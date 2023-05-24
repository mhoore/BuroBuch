from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import ModelForm
from django.forms.utils import ErrorList
import datetime
from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'

class BookingCreateForm(ModelForm):
    empty_label = '---'
    building = forms.ModelChoiceField(queryset=Building.objects.all(), empty_label=empty_label)
    department = forms.ChoiceField(choices=[('', empty_label),])
    room = forms.ChoiceField(choices=[('', empty_label),])
    desk = forms.ChoiceField(choices=[('', empty_label),])

    class Meta:
        model = Booking
        fields = ['building', 'department', 'room', 'desk', 'date']
        widgets = {
            'date': DateInput(),
            'initial': datetime.date.today()
        }

    class Media:
        js = ("booking/js/booking_form.js", )

    def __init__(self, *args, **kwargs):
        super(BookingCreateForm, self).__init__(*args, **kwargs)
        self.fields['date'].initial = datetime.date.today()
