from django.contrib import admin
from django.utils.html import format_html
from .models import RentalProperty, Booking, Availability, GalleryImage


# Inline для изображений галереи
class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1
    fields = ('image', 'thumbnail')
    readonly_fields = ('thumbnail',)

    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />',
                obj.image.url
            )
        return "-"
    thumbnail.short_description = 'Preview'


# Админка для Вилл
@admin.register(RentalProperty)
class RentalPropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price_per_night', 'thumbnail')
    search_fields = ('title', 'location')
    list_filter = ('location',)
    inlines = [GalleryImageInline]

    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />',
                obj.image.url
            )
        return "-"
    thumbnail.short_description = 'Main Image'


# Админка для Бронирований
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('property', 'first_name', 'last_name', 'email', 'phone', 'guests', 'date_range', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'property__title')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


# Админка для Доступности
@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('property', 'date')
    search_fields = ('property__title',)
    list_filter = ('date', 'property')
    ordering = ('date',)
