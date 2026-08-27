import logging
import requests
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)


def log_notification(notification_type, recipient, status, order=None, error=''):
    from .models import NotificationLog
    NotificationLog.objects.create(
        order=order,
        notification_type=notification_type,
        recipient=recipient,
        status=status,
        error_message=error,
    )


def format_order_items(order):
    items = []
    for item in order.items.select_related('food').all():
        items.append({
            'name': item.food.name,
            'quantity': item.quantity,
            'price': item.price,
            'subtotal': item.price * item.quantity,
        })
    return items


def send_customer_confirmation(order):
    if not order.email:
        log_notification('CUSTOMER_EMAIL', '(no email)', 'SKIPPED', order, 'No email provided')
        return False

    items = format_order_items(order)
    context = {
        'order': order,
        'items': items,
        'restaurant_name': 'ClockTower Food Service',
    }

    try:
        html_content = render_to_string('emails/customer_confirmation.html', context)
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(
            subject=f'Order Confirmation #{order.order_num} - ClockTower',
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order.email],
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send(fail_silently=False)

        log_notification('CUSTOMER_EMAIL', order.email, 'SENT', order)
        return True
    except Exception as e:
        logger.error(f'Customer email failed for {order.order_num}: {e}')
        log_notification('CUSTOMER_EMAIL', order.email, 'FAILED', order, str(e))
        return False


def send_internal_notification(order):
    recipient = settings.ORDER_NOTIFICATION_EMAIL
    if not recipient:
        log_notification('INTERNAL_EMAIL', '(not configured)', 'SKIPPED', order, 'ORDER_NOTIFICATION_EMAIL not set')
        return False

    items = format_order_items(order)
    context = {
        'order': order,
        'items': items,
        'restaurant_name': 'ClockTower Food Service',
    }

    try:
        html_content = render_to_string('emails/internal_notification.html', context)
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(
            subject=f'New Order #{order.order_num} - TSh {order.total:,}',
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient],
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send(fail_silently=False)

        log_notification('INTERNAL_EMAIL', recipient, 'SENT', order)
        return True
    except Exception as e:
        logger.error(f'Internal email failed for {order.order_num}: {e}')
        log_notification('INTERNAL_EMAIL', recipient, 'FAILED', order, str(e))
        return False


def send_whatsapp_message(phone, message):
    api_url = settings.WHATSAPP_API_URL
    api_token = settings.WHATSAPP_API_TOKEN
    phone_id = settings.WHATSAPP_PHONE_NUMBER_ID

    if not all([api_url, api_token, phone_id]):
        return False

    try:
        headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json',
        }
        payload = {
            'messaging_product': 'whatsapp',
            'to': phone,
            'type': 'text',
            'text': {'body': message},
        }
        response = requests.post(
            f'{api_url}/{phone_id}/messages',
            json=payload,
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()
        return True
    except Exception as e:
        logger.error(f'WhatsApp API failed to {phone}: {e}')
        return False


def build_whatsapp_message(order):
    items = format_order_items(order)
    item_lines = '\n'.join([
        f"  * {i['name']} x{i['quantity']} — TSh {i['subtotal']:,}"
        for i in items
    ])

    msg = f"""NEW E-MENU ORDER

Order Number: #{order.order_num}
Customer Name: {order.name}
Customer Phone: {order.phone}
Table/Room: {order.table_location or 'N/A'}

ORDER ITEMS:
{item_lines}

Subtotal: TSh {order.total:,}
Payment Status: {order.get_payment_status_display()}
Order Status: NEW

Date/Time: {order.created_at.strftime('%d %b %Y, %H:%M')}
Payment Method: {order.get_payment_status_display()}
"""
    return msg.strip()


def send_whatsapp_notifications(order):
    message = build_whatsapp_message(order)
    recipients = {
        'WHATSAPP_ADMIN_1': settings.WHATSAPP_ADMIN_1,
        'WHATSAPP_ADMIN_2': settings.WHATSAPP_ADMIN_2,
        'WHATSAPP_RECEPTION': settings.WHATSAPP_RECEPTION,
    }

    results = {}
    for notif_type, phone in recipients.items():
        if not phone:
            log_notification(notif_type, '(not configured)', 'SKIPPED', order, 'Phone number not set')
            results[notif_type] = False
            continue

        if settings.WHATSAPP_API_URL:
            success = send_whatsapp_message(phone, message)
            status = 'SENT' if success else 'FAILED'
        else:
            status = 'SKIPPED'
            success = False
            logger.info(f'WhatsApp API not configured, skipping {notif_type} to {phone}')

        log_notification(notif_type, phone, status, order, '' if success else 'WhatsApp API not configured')
        results[notif_type] = success

    return results


def send_order_notifications(order):
    send_customer_confirmation(order)
    send_internal_notification(order)
    send_whatsapp_notifications(order)
