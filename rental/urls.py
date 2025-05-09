from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'rental'

urlpatterns = [
    path('', views.property_list, name='home'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('booking-success/<int:booking_id>/', views.booking_success, name='booking_success'),
    path('checkout/<int:booking_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('payment-success/', TemplateView.as_view(template_name='rental/success.html'), name='payment_success'),
    path('accommodation/', views.accommodation, name='accommodation'),
    path('destinations/', views.destinations, name='destinations'),
    path('services/', views.services, name='services'),
    path('experiences/', views.experiences, name='experiences'),
    path('offers/', views.offers, name='offers'),
    path('blog/', views.blog, name='blog'),
]
