import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clocktower_backend.settings')
django.setup()

from core.models import NotificationLog, Notification, Order, OrderItem

print("=" * 60)
print("  NOTIFICATION LOGS FROM DATABASE")
print("=" * 60)

logs = NotificationLog.objects.all()
print(f"\nTotal logs: {logs.count()}")
for log in logs:
    print(f"  [{log.created_at.strftime('%d %b %H:%M')}] {log.notification_type} -> {log.recipient} [{log.status}]")
    if log.error_message:
        print(f"    Error: {log.error_message[:100]}")

print("\n" + "=" * 60)
print("  IN-APP NOTIFICATIONS")
print("=" * 60)

notifs = Notification.objects.all()
print(f"\nTotal: {notifs.count()}")
for n in notifs:
    print(f"  [{n.created_at.strftime('%d %b %H:%M')}] {n.title}")
    print(f"    {n.detail[:120]}")

print("\n" + "=" * 60)
print("  ORDERS SUMMARY")
print("=" * 60)

orders = Order.objects.all()
print(f"\nTotal orders: {orders.count()}")
for o in orders:
    items = list(o.items.select_related('food').all())
    item_str = ', '.join([f"{i.food.name} x{i.quantity}" for i in items])
    print(f"  #{o.order_num} | {o.name} | {o.phone} | TSh {o.total:,} | {o.status}/{o.payment_status}")
    print(f"    Items: {item_str}")

print("\n" + "=" * 60)
print("  EMAIL CONFIG STATUS")
print("=" * 60)

from django.conf import settings
print(f"  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER or '(EMPTY - not configured)'}")
print(f"  EMAIL_HOST_PASSWORD: {'SET' if settings.EMAIL_HOST_PASSWORD else '(EMPTY - not configured)'}")
print(f"  DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
print(f"  ORDER_NOTIFICATION_EMAIL: {settings.ORDER_NOTIFICATION_EMAIL or '(EMPTY - not configured)'}")

print("\n" + "=" * 60)
print("  WHATSAPP CONFIG STATUS")
print("=" * 60)
print(f"  WHATSAPP_ADMIN_1: {settings.WHATSAPP_ADMIN_1 or '(EMPTY - not configured)'}")
print(f"  WHATSAPP_ADMIN_2: {settings.WHATSAPP_ADMIN_2 or '(EMPTY - not configured)'}")
print(f"  WHATSAPP_RECEPTION: {settings.WHATSAPP_RECEPTION or '(EMPTY - not configured)'}")
print(f"  WHATSAPP_API_URL: {settings.WHATSAPP_API_URL or '(EMPTY - not configured)'}")
print(f"  WHATSAPP_API_TOKEN: {'SET' if settings.WHATSAPP_API_TOKEN else '(EMPTY - not configured)'}")
print(f"  WHATSAPP_PHONE_NUMBER_ID: {settings.WHATSAPP_PHONE_NUMBER_ID or '(EMPTY - not configured)'}")
