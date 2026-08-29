import sys

from datetime import date, timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.db.models import Sum

from core.models import ActivityLog, Order


def growth(cur, prev):
    if prev <= 0:
        return 0
    return round((cur - prev) / prev * 100)


def month_range(y, m):
    start = date(y, m, 1)
    if m == 12:
        end = date(y + 1, 1, 1) - timedelta(days=1)
    else:
        end = date(y, m + 1, 1) - timedelta(days=1)
    return start, end


class Command(BaseCommand):
    help = ('Generate end-of-month business report (revenue, orders, customers, growth). '
            'Use --month YYYY-MM to pick a month (default: last closed month).')

    def add_arguments(self, parser):
        parser.add_argument('--month', help='Month to report, format YYYY-MM (default previous month)')

    def handle(self, *args, **opts):
        today = date.today()
        if opts['month']:
            try:
                y, m = (int(x) for x in opts['month'].split('-'))
            except (ValueError, TypeError):
                self.stderr.write('--month must be in format YYYY-MM')
                sys.exit(1)
        else:
            first = today.replace(day=1)
            prev = first - timedelta(days=1)
            y, m = prev.year, prev.month

        start, end = month_range(y, m)
        if end > today:
            self.stdout.write(self.style.WARNING('Mwezi haujamalizika; ripoti ni ya hadi leo.'))

        def rev(qs):
            return qs.aggregate(s=Sum('total'))['s'] or 0

        orders = Order.objects.filter(date__gte=start, date__lte=end)
        prev_end = start - timedelta(days=1)
        prev_start = prev_end.replace(day=1)
        prev_orders = Order.objects.filter(date__gte=prev_start, date__lte=prev_end)

        revenue = rev(orders)
        count = orders.count()
        customers = orders.values('phone').distinct().count()
        avg = revenue // count if count else 0
        g = growth(revenue, rev(prev_orders))

        lines = [
            f'RIPOTI YA BIASHARA - {start.strftime("%B %Y")}',
            '-' * 46,
            f'Mapato: TSh {revenue:,}',
            f'Maagizo: {count}',
            f'Wateja: {customers}',
            f'Wastani wa Agizo: TSh {avg:,}',
            f'Ukuaji vs Mwezi Uliotangulia: {g:+}%',
        ]
        for line in lines:
            self.stdout.write(line)

        recipients = []
        order_email = getattr(settings, 'ORDER_NOTIFICATION_EMAIL', '')
        if order_email:
            recipients.append(order_email)
        for _, addr in getattr(settings, 'ADMINS', []):
            recipients.append(addr)

        if recipients:
            try:
                send_mail(
                    subject=f'Ripoti ya Mwezi - {start.strftime("%B %Y")}',
                    message='\n'.join(lines),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=list(set(recipients)),
                    fail_silently=True,
                )
                self.stdout.write(self.style.SUCCESS('Ripoti imetumwa kwa barua pepe: ' + ', '.join(set(recipients))))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Barua pepe haikutumwa: {e}'))

        ActivityLog.objects.create(
            user=None,
            action='Ripoti ya Mwezi',
            detail=f'{start.strftime("%B %Y")}: TSh {revenue:,}, maagizo {count}, ukuaji {g:+}%',
        )
        self.stdout.write(self.style.SUCCESS('Ripoti imeandikwa kwenye Activity Log.'))