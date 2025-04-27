from django.db import models


class RentalProperty(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    address = models.CharField(max_length=255)

    def str(self):
        return self.title


class Availability(models.Model):
    property = models.ForeignKey(RentalProperty, on_delete=models.CASCADE)
    date = models.DateField()
    is_available = models.BooleanField(default=True)

    def str(self):
        return f"{self.property.title} - {self.date}"


class Booking(models.Model):
    property = models.ForeignKey(RentalProperty, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20)
    check_in = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    def str(self):
        return f"Booking by {self.name} for {self.property.title}"
