from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import ModelForm
from django.forms.utils import ErrorList
from django.core.exceptions import ValidationError
import datetime
from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'

class BookingCreateForm(ModelForm):
    user = None
    empty_label = '---'
    building = forms.ModelChoiceField(queryset=Building.objects.all(), empty_label=empty_label)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label=empty_label)
    room = forms.ModelChoiceField(queryset=Room.objects.all(), empty_label=empty_label)
    desk = forms.ModelChoiceField(queryset=Desk.objects.all(), empty_label=empty_label)

    class Meta:
        model = Booking
        fields = ['date', 'building', 'department', 'room', 'desk', ]
        widgets = {
            'date': DateInput(),
            'initial': datetime.date.today()
        }

    class Media:
        js = ("booking/js/booking_form.js", )

    def __init__(self, *args, **kwargs):
        self.user = User.objects.get(username=kwargs.pop('username'))
        super(BookingCreateForm, self).__init__(*args, **kwargs)
        self.fields['date'].initial = datetime.date.today()

    def clean(self):
        cleaned_data = super().clean()
        self.instance.user = self.user

        if Booking.objects.filter(user=self.user, date=cleaned_data['date']).exists():
            raise ValidationError("A booking already exists for the chosen date.")
