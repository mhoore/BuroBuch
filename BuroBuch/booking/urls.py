from django.urls import path
from .views import (
    BookingListView,
    BookingDetailView,
    BookingDeleteView,
    BookingCreateView,
)
from . import views

urlpatterns = [
    path('', BookingListView.as_view(), name='booking-home'),
    path('booking/<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    path('booking/new/', BookingCreateView.as_view(), name='booking-create'),
    path('booking/<int:pk>/delete/', BookingDeleteView.as_view(), name='booking-delete'),
    path('booking/get_choices/', views.get_choices, name = 'booking-get-choices'),
    path('about/', views.about, name='booking-about'),
]
