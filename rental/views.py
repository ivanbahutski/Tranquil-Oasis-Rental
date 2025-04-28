from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import RentalProperty, Booking, Availability
from datetime import datetime, timedelta
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


def property_list(request):
    properties = RentalProperty.objects.all()
    return render(request, 'rental/property_list.html', {'properties': properties})


def property_detail(request, pk):
    property = get_object_or_404(RentalProperty, pk=pk)
    availabilities = Availability.objects.filter(property=property).order_by('date')
    bookings = Booking.objects.filter(property=property)

    booked_dates = []
    for booking in bookings:
        if booking.check_in and booking.check_out:
            current_date = booking.check_in
            while current_date <= booking.check_out:
                booked_dates.append(current_date.strftime('%Y-%m-%d'))
                current_date += timedelta(days=1)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date_range = request.POST.get('date_range')

        if date_range:
            parts = date_range.split(' to ')
            if len(parts) == 2:
                check_in = datetime.strptime(parts[0], "%Y-%m-%d").date()
                check_out = datetime.strptime(parts[1], "%Y-%m-%d").date()
            else:
                check_in = check_out = datetime.strptime(date_range, "%Y-%m-%d").date()
        else:
            check_in = check_out = None

        booking = Booking.objects.create(
            property=property,
            name=name,
            email=email,
            phone=phone,
            check_in=check_in,
            check_out=check_out,
            is_paid=False,
        )
        # --- ОТПРАВКА ПИСЬМА ---
        subject = "New Booking Request"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = settings.ADMIN_EMAIL  # сюда приходит письмо (например, твой email администратора)
        text_content = f"New booking:\n\nProperty: {property.title}\nName: {name}\nEmail: {email}\nPhone: {phone}\nCheck-in: {check_in}\nCheck-out: {check_out}"
        html_content = f"""
        <h2>New Booking Request</h2>
        <p><strong>Property:</strong> {property.title}</p>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Phone:</strong> {phone}</p>
        <p><strong>Check-in:</strong> {check_in}</p>
        <p><strong>Check-out:</strong> {check_out}</p>
        """

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        # --- КОНЕЦ ОТПРАВКИ ПИСЬМА ---
        return redirect('booking_success', booking_id=booking.id)

    return render(request, 'rental/property_detail.html', {
        'property': property,
        'availabilities': availabilities,
        'booked_dates': booked_dates,
    })


def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if booking.check_in and booking.check_out:
        nights = (booking.check_out - booking.check_in).days
    else:
        nights = 0

    return render(request, 'rental/booking_success.html', {
        'booking': booking,
        'nights': nights,
    })


def create_checkout_session(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    nights = (booking.check_out - booking.check_in).days
    amount = int(booking.property.price_per_night * nights * 100)  # в центах

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': f"Booking {booking.property.title}",
                },
                'unit_amount': amount,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('booking_success', kwargs={'booking_id': booking.id})
        ),
        cancel_url=request.build_absolute_uri(
            reverse('property_detail', kwargs={'pk': booking.property.id})
        ),
    )
    return redirect(session.url)


def home(request):
    return render(request, 'home.html')


def accommodation(request):
    return render(request, 'accommodation.html')


def destinations(request):
    return render(request, 'destinations.html')


def services(request):
    return render(request, 'services.html')


def experiences(request):
    return render(request, 'experiences.html')


def offers(request):
    return render(request, 'offers.html')


def blog(request):
    return render(request, 'blog.html')
