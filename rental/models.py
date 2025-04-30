from django.utils import timezone
from PIL import Image
from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
import os


class RentalProperty(models.Model):
    title = models.CharField(max_length=200, default='', blank=True)
    location = models.CharField(max_length=200, default='', blank=True)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='property_images/', blank=True, null=True)

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"

    def str(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            max_size = (1200, 800)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            img.save(self.image.path)


class GalleryImage(models.Model):
    property = models.ForeignKey(RentalProperty, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='property_gallery/')

    class Meta:
        verbose_name = 'Gallery image'
        verbose_name_plural = 'Gallery images'

    def str(self):
        return f"Image for {self.property.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            max_size = (1200, 800)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            img.save(self.image.path)


class PropertyImage(models.Model):
    property = models.ForeignKey(RentalProperty, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')

    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"

    def str(self):
        return f"Фото для {self.property.title}"


class Availability(models.Model):
    property = models.ForeignKey(RentalProperty, on_delete=models.CASCADE)
    date = models.DateField()
    is_available = models.BooleanField(default=True)

    def str(self):
        return f"{self.property.title} - {self.date}"


class Booking(models.Model):
    property = models.ForeignKey(RentalProperty, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    guests = models.PositiveIntegerField(default=1)
    message = models.TextField(blank=True)
    date_range = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def str(self):
        return f"Booking by {self.first_name}{self.last_name} for {self.property.title}"


# Автоматическое удаление старого фото при замене
@receiver(pre_save, sender=RentalProperty)
def auto_delete_old_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_image = RentalProperty.objects.get(pk=instance.pk).image
    except RentalProperty.DoesNotExist:
        return False

    new_image = instance.image
    if old_image and old_image != new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)


# Автоматическое удаление фото при удалении объекта
@receiver(post_delete, sender=RentalProperty)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
