from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import *

@shared_task
def send_order_confirmation_email(order_id, user_email):
    order = Order.objects.get(id=order_id)
    subject = 'Order Confirmation'
    html_message = render_to_string('order.html', {'order': order})
    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        html_message=html_message,
    )




