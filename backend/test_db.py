import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clocktower_backend.settings')
django.setup()
from core.models import Order
for o in Order.objects.all().order_by('id'):
    print(f"#{o.order_num} | {o.name} | payment={o.payment_method} | status={o.status}")
