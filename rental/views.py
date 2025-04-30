import stripe
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from datetime import timedelta, datetime
from .models import RentalProperty, Booking, Availability

stripe.api_key = settings.STRIPE_SECRET_KEY


def property_list(request):
    """Список всех объектов аренды."""
    props = RentalProperty.objects.all()
    return render(request, 'rental/property_list.html', {
        'props': props,
    })


def property_detail(request, pk):
    prop = get_object_or_404(RentalProperty, pk=pk)
    # собираем занятые даты
    booked_dates = []
    for b in Booking.objects.filter(rental_property=prop):
        cur = b.check_in
        while cur < b.check_out:
            booked_dates.append(cur.strftime('%Y-%m-%d'))
            cur += timedelta(days=1)

    if request.method == 'POST':
        # вытаскиваем поля формы
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        add_bed = bool(request.POST.get('add_bed'))
        high_chair = bool(request.POST.get('high_chair'))
        try:
            adults = int(request.POST.get('adults', 1))
            children = int(request.POST.get('children', 0))
            infants = int(request.POST.get('infants', 0))
        except ValueError:
            messages.error(request, "Введите корректное количество гостей.")
            return redirect('rental:property_detail', pk=prop.pk)

        try:
            check_in = datetime.strptime(request.POST['check_in'], '%Y-%m-%d').date()
            check_out = datetime.strptime(request.POST['check_out'], '%Y-%m-%d').date()
        except (KeyError, ValueError):
            messages.error(request, "Выберите корректные даты.")
            return redirect('rental:property_detail', pk=prop.pk)
        if check_in >= check_out:
            messages.error(request, "Дата выезда должна быть после даты заезда.")
            return redirect('rental:property_detail', pk=prop.pk)

        # сохраняем бронь
        booking = Booking.objects.create(
            rental_property=prop,
            first_name=first_name, last_name=last_name,
            email=email, phone=phone,
            add_bed=add_bed,
            high_chair=high_chair,
            adults=adults, children=children, infants=infants,
            check_in=check_in, check_out=check_out,
            created_at=timezone.now(),
        )
        # уведомляем админа
        subject = f"Новая бронь: {prop.title}"
        text = (
            f"Объект: {prop.title}\n"
            f"Гость: {first_name} {last_name}\n"
            f"Email: {email}, Телефон: {phone}\n"
            f"Взрослых: {adults}, детей: {children}, младенцев: {infants}\n"
            f"Заезд: {check_in}, выезд: {check_out}\n"
            f"Ночей: {booking.nights}\n"
            f"Кровать: {'Да' if booking.add_bed else 'Нет'}\n"
            f"Кресло: {'Да' if booking.high_chair else 'Нет'}\n"
            f"Итог: {booking.total_cost}"
        )
        html = text.replace("\n", "<br>")
        msg = EmailMultiAlternatives(subject, text, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL])
        msg.attach_alternative(html, "text/html")
        msg.send()

        messages.success(request, "Бронь успешно создана! Подтверждение отправлено на почту.")
        return redirect('rental:booking_success', booking_id=booking.id)

    return render(request, 'rental/property_detail.html', {
        'prop': prop,
        'booked_dates': booked_dates,
    })


def booking_success(request, booking_id):
    """Страница успешного создания брони."""
    b = get_object_or_404(Booking, pk=booking_id)
    return render(request, 'rental/booking_success.html', {
        'booking':   b,
        'nights':    b.nights,
        'total':     b.total_cost,
    })


def create_checkout_session(request, booking_id):
    """Создать сессию Stripe для оплаты."""
    b = get_object_or_404(Booking, pk=booking_id)
    amount_eur = int(b.total_cost * 100)  # сумма в центах

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'product_data': {'name': f"Booking {b.rental_property.title}"},
                'unit_amount': amount_eur,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('rental:payment_success')),
        cancel_url=request.build_absolute_uri(reverse('rental:property_detail', kwargs={'pk': b.rental_property.pk})),
    )
    return redirect(session.url)


# === Дополнительные страницы меню / блог ===

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
    # если ещё нет модели поста, просто выводим статический шаблон
    return render(request, 'menu/blog.html')
