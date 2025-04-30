from django.contrib import admin
from django.utils.html import format_html

from .models import RentalProperty, GalleryImage, Availability, Booking


# Inline для галереи картинок
class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1
    readonly_fields = ('thumbnail',)
    fields = ('image', 'thumbnail')

    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />',
                obj.image.url
            )
        return "-"
    thumbnail.short_description = 'Preview'


@admin.register(RentalProperty)
class RentalPropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price_per_night',  'thumbnail')
    search_fields = ('title', 'location')
    list_filter = ('location',)
    inlines = [GalleryImageInline]

    def thumbnail(self, obj):
        if obj.main_image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />',
                obj.main_image.url
            )
        return "-"
    thumbnail.short_description = 'Main Image'


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('rental_property', 'date', 'is_available')
    search_fields = ('rental_property__title',)
    list_filter = ('date', 'rental_property')
    ordering = ('date',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'rental_property', 'first_name', 'last_name', 'email', 'phone',
        'adults', 'children', 'infants',
        'add_bed', 'high_chair',
        'check_in', 'check_out', 'nights', 'created_at'
    )
    search_fields = (
        'first_name', 'last_name', 'email', 'phone',
        'rental_property__title'
    )
    list_filter = (
        'created_at', 'rental_property', 'check_in', 'check_out',
        'add_bed', 'high_chair'
    )
    ordering = ('-created_at',)

    # атрибут nights — свойство модели
    def nights(self, obj):
        return obj.nights
    nights.short_description = 'Nights'
