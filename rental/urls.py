from django.urls import path
from django.views.generic import TemplateView

from .views import property_list, property_detail, booking_success, create_checkout_session

urlpatterns = [
    path('', property_list, name='property_list'),
    path('property/<int:pk>/', property_detail, name='property_detail'),
    path('booking-success/<int:booking_id>/', booking_success, name='booking_success'),
    path('create-checkout-session/<int:booking_id>/', create_checkout_session, name='create_checkout_session'),
    path('success/', TemplateView.as_view(template_name='rental/success.html'), name='payment_success'),
    path('cancel/', TemplateView.as_view(template_name='rental/cancel.html'), name='payment_cancel'),
]
