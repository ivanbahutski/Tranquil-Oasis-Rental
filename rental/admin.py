from django.contrib import admin
from .models import RentalProperty, Booking, Availability

@admin.register(RentalProperty)
class RentalPropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'price_per_night', 'address')

@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('property', 'date')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('property', 'name', 'email', 'phone', 'check_in', 'check_out', 'is_paid')
    list_filter = ('is_paid', 'check_in', 'check_out')
    search_fields = ('name', 'email', 'phone', 'property__title')