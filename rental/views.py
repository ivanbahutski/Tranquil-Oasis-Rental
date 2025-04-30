from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from .models import RentalProperty, Booking, Availability
from datetime import datetime, timedelta
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

    # Блокируем забронированные даты
    booked_dates = []
    for booking in bookings:
        if booking.date_range:
            try:
                dates = booking.date_range.split(' to ')
                if len(dates) == 2:
                    start = datetime.strptime(dates[0], "%Y-%m-%d").date()
                    end = datetime.strptime(dates[1], "%Y-%m-%d").date()
                    current = start
                    while current <= end:
                        booked_dates.append(current.strftime('%Y-%m-%d'))
                        current += timedelta(days=1)
            except Exception:
                continue

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        guests = request.POST.get('guests')
        message = request.POST.get('message')
        date_range = request.POST.get('date_range')

        # Разбиваем диапазон дат
        dates = date_range.split(' to ')
        if len(dates) == 2:
            try:
                check_in_date = datetime.strptime(dates[0], "%Y-%m-%d").date()
                check_out_date = datetime.strptime(dates[1], "%Y-%m-%d").date()
            except ValueError:
                check_in_date = check_out_date = None
        else:
            check_in_date = check_out_date = None

        # Проверка диапазона дат
        if not check_in_date or not check_out_date:
            messages.error(request, "Error selecting dates. Please choose a valid range.")
            return redirect('property_detail', pk=property.pk)

        # Сохраняем бронь
        booking = Booking.objects.create(
            property=property,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            guests=guests,
            message=message,
            date_range=date_range
        )

        # Форматируем даты для письма
        check_in_str = check_in_date.strftime("%d %B %Y")
        check_out_str = check_out_date.strftime("%d %B %Y")

        # Создаём текст письма
        subject = "New Booking Request"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = settings.ADMIN_EMAIL

        text_content = (
            f"New Booking:\n\n"
            f"Property: {property.title}\n"
            f"Name: {first_name} {last_name}\n"
            f"Email: {email}\n"
            f"Phone: {phone}\n"
            f"Guests: {guests}\n"
            f"Special requests: {message}\n"
            f"Check-in: {check_in_str}\n"
            f"Check-out: {check_out_str}"
        )

        html_content = f"""
            <h2>New Booking</h2>
            <p><strong>Property:</strong> {property.title}</p>
            <p><strong>Name:</strong> {first_name} {last_name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Phone:</strong> {phone}</p>
            <p><strong>Guests:</strong> {guests}</p>
            <p><strong>Special requests:</strong> {message}</p>
            <p><strong>Check-in:</strong> {check_in_str}</p>
            <p><strong>Check-out:</strong> {check_out_str}</p>
        """

        # Отправляем email
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        messages.success(request, "Your booking request has been sent successfully!")
        return redirect('booking_success', booking_id=booking.id)

    return render(request, 'rental/property_detail.html',
        {
            'property': property,
            'availabilities': availabilities,
            'booked_dates': booked_dates
        })


def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)

    nights = 0
    check_in_str = ''
    check_out_str = ''

    if booking.date_range:
        dates = booking.date_range.split(' to ')
        if len(dates) == 2:
            try:
                check_in_date = datetime.strptime(dates[0], "%Y-%m-%d").date()
                check_out_date = datetime.strptime(dates[1], "%Y-%m-%d").date()
                nights = (check_out_date - check_in_date).days

                # Форматируем даты для красивого отображения
                check_in_str = check_in_date.strftime("%d %B %Y")
                check_out_str = check_out_date.strftime("%d %B %Y")
            except ValueError:
                nights = 0

    return render(request, 'rental/booking_success.html', {
        'booking': booking,
        'nights': nights,
        'check_in': check_in_str,
        'check_out': check_out_str,
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


def accommodation(request):
    return render(request, 'menu/accommodation.html')


def destinations(request):
    return render(request, 'menu/destinations.html')


def services(request):
    return render(request, 'menu/services.html')


def experiences(request):
    return render(request, 'menu/experiences.html')


def offers(request):
    return render(request, 'menu/offers.html')


def blog(request):
    return render(request, 'menu/blog.html')
