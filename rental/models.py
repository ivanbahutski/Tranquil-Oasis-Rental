from decimal import Decimal

from django.db import models
from django.utils import timezone
from django.urls import reverse
from PIL import Image


class RentalProperty(models.Model):
    title = models.CharField(max_length=200, unique=True)
    location = models.CharField(max_length=200)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    cleaning_fee = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal('200.00'),
        help_text="Уборка (включается в итоговую сумму брони)"
    )
    description = models.TextField(blank=True)
    main_image = models.ImageField(upload_to='properties/main/', blank=True, null=True)

    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['price_per_night']),
        ]
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # теперь по pk
        return reverse('rental:property_detail', kwargs={'pk': self.pk})



    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.main_image:
            img = Image.open(self.main_image.path)
            img.thumbnail((1200, 800), Image.Resampling.LANCZOS)
            img.save(self.main_image.path)


class GalleryImage(models.Model):
    rental_property = models.ForeignKey(RentalProperty, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='properties/gallery/')

    class Meta:
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'

    def __str__(self):
        return f"Image for {self.rental_property.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            img.thumbnail((1200, 800), Image.Resampling.LANCZOS)
            img.save(self.image.path)


class Booking(models.Model):
    # Age cutoffs: infant 0–2, child 3–12, adult 13+
    adults = models.PositiveIntegerField(default=1, help_text='Guests aged 13 and above')
    children = models.PositiveIntegerField(default=0, help_text='Guests aged 3 to 12')
    infants = models.PositiveIntegerField(default=0, help_text='Guests aged up to 2 (crib/high chair)')

    rental_property = models.ForeignKey(
                        RentalProperty,
                        on_delete=models.CASCADE,
                        db_column='property_id',
                        related_name='bookings',
                        verbose_name='property',)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)

    check_in = models.DateField()
    check_out = models.DateField()

    add_bed = models.BooleanField(default=False, help_text='Additional bed (€50/night)')
    high_chair = models.BooleanField(default=False, help_text='High chair (€10 flat)')
    cleaning_fee = models.DecimalField(max_digits=8, decimal_places=2, default=200.00)

    message = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(check=models.Q(check_out__gt=models.F('check_in')), name='check_out_after_check_in'),
        ]
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        return f"Booking by {self.first_name} {self.last_name} for {self.rental_property.title}"

    @property
    def nights(self):
        return (self.check_out - self.check_in).days

    @property
    def bed_cost(self):
        # 15 € за ночь
        return Decimal('15.00') * self.nights if self.add_bed else Decimal('0.00')

    @property
    def chair_cost(self):
        # 5 € за ночь
        return Decimal('5.00') * self.nights if self.high_chair else Decimal('0.00')

    @property
    def base_cost(self):
        base = self.nights * self.rental_property.price_per_night
        return base

    @property
    def total_cost(self):
        # доп. услуги и плата за уборку из свойства недвижимости
        return self.base_cost + self.bed_cost + self.chair_cost + self.rental_property.cleaning_fee


class Availability(models.Model):
    rental_property = models.ForeignKey(
        RentalProperty,
        on_delete=models.CASCADE,
        db_column='property_id',
        related_name='availabilities',
        verbose_name='property',
    )
    date = models.DateField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('rental_property', 'date')
        ordering = ['date']
        indexes = [models.Index(fields=['rental_property', 'date'])]
        verbose_name = 'Availability'
        verbose_name_plural = 'Availabilities'

    def __str__(self):
        status = 'Available' if self.is_available else 'Booked'
        return f"{self.rental_property.title}: {status} on {self.date}"
