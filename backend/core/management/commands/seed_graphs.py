import random
from datetime import date, datetime, time, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import Food, Order, OrderItem

NAMES = [
    'Amina Hassan', 'Juma Mwinyi', 'Neema Joseph', 'Baraka Komba', 'Zainabu Ali',
    'Daudi Peter', 'Hawa Said', 'Emmanuel Mtui', 'Rehema John', 'Salim Omar',
    'Asha Rajabu', 'Godfrey Mushi', 'Amina Kiteto', 'Mwanaidi Ramadhani',
]
PLACES = ['Meza 1', 'Meza 2', 'Meza 3', 'Meza 5', 'Balcony', 'Karibu Kona', 'Chumba', 'Lounge']
METHODS = ['mpesa', 'mpesa', 'cash', 'tigo', 'cash', 'mpesa', 'bank']


class Command(BaseCommand):
    help = 'Seed sample sales history so all dashboard charts (Leo/Wiki/Mwezi/Mwaka) show data'

    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, default=365, help='How many days back to seed (default 365)')
        parser.add_argument('--force', action='store_true',
                            help='Also add orders on days that already have enough (default skips them)')

    def handle(self, *args, **options):
        foods = list(Food.objects.filter(is_active=True))
        if not foods:
            self.stderr.write('Hakuna Food kwenye mfumo. Endesha: python manage.py seed kwanza.')
            return

        random.seed(2026)
        today = date.today()
        start = today - timedelta(days=options['days'])
        now = timezone.localtime()
        created = 0
        skipped = 0

        self.stdout.write(f'Seed data kutoka {start} hadi {today} ...')

        days = (today - start).days
        for i in range(days + 1):
            day = start + timedelta(days=i)
            factor = 0.5 + (i / max(days, 1)) * 1.6  # upward business trend
            base = {0: 5, 1: 5, 2: 6, 3: 6, 4: 8, 5: 9, 6: 7}[day.weekday()]
            target = max(2, int(base * factor) + random.randint(-1, 2))
            existing = Order.objects.filter(date=day).count()
            need = max(0, target - existing)
            if existing >= target and not options['force']:
                skipped += 1
                continue

            for _ in range(need):
                order = self._make_order(day, foods, now)
                if order:
                    created += 1

        self.stdout.write(self.style.SUCCESS(f'Orders zilizoundwa: {created}'))
        self.stdout.write(self.style.SUCCESS(f'Siku zilizorukwa (tayari zinafanikiwa): {skipped}'))

    def _make_order(self, day, foods, now):
        random.seed(int(day.toordinal()) * 999 + random.randint(0, 50))
        hour = random.choices(
            [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
            weights=[1, 1, 1, 1, 3, 3, 2, 1, 1, 2, 3, 4, 3, 2],
        )[0]
        minute = random.randint(0, 59)
        if day == now.date():
            hour = min(hour, now.hour)
            minute = min(minute, now.minute) if hour == now.hour else minute

        items = random.sample(foods, random.randint(1, 3))
        total = 0
        lines = []
        for f in items:
            qty = random.randint(1, 4)
            total += f.price * qty
            lines.append((f, qty))

        order = Order.objects.create(
            name=random.choice(NAMES),
            phone=f'07{random.randint(10000000, 99999999)}',
            table_location=random.choice(PLACES),
            payment_method=random.choice(METHODS),
            status=random.choice(['delivered', 'delivered', 'confirmed', 'paid']),
            payment_status=random.choice(['paid', 'paid', 'paid', 'unpaid']),
            total=total,
            date=day,
            created_at=timezone.make_aware(datetime.combine(day, time(hour, minute))),
        )
        OrderItem.objects.bulk_create([
            OrderItem(order=order, food=f, quantity=qty, price=f.price) for f, qty in lines
        ])
        return order