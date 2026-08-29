import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import date, timedelta
from .models import User, Category, Food, Order, OrderItem, Notification, Comment, ActivityLog, Expense
from .forms import (LoginForm, ForgotPasswordForm, FoodForm, UserForm,
                    ProfileForm, ChangePasswordForm, CommentForm, SettingsForm)


def get_setting(key, default=''):
    from django.conf import settings
    return getattr(settings, key, default)


def log_activity(user, action, detail=''):
    ActivityLog.objects.create(user=user, action=action, detail=detail)


def push_notification(title, detail=''):
    Notification.objects.create(title=title, detail=detail)


def clear_caches():
    """Purge any server-side caches (menu, dashboard stats, notifications,
    etc.) right after an order is placed so the admin panel and the user
    site always show fresh data. Safe no-op when caching isn't configured.
    """
    try:
        from django.core.cache import cache
        cache.clear()
        for key in ('foods_api', 'admin_dashboard_stats', 'notifications_list'):
            cache.delete(key)
    except Exception:
        pass


def generate_order_num():
    last = Order.objects.order_by('-id').first()
    num = (last.id + 1) if last else 1
    return f"CTF-{num:06d}"


# ========== AUTH ==========

def login_view(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user and user.is_active:
            login(request, user)
            log_activity(user, 'Ameingia', f'{user.get_full_name() or user.username} ameingia')
            return redirect('admin_dashboard')
        return render(request, 'core/login.html', {'error': 'Username au password si sahihi.'})

    return render(request, 'core/login.html')


def forgot_password_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        answer = request.POST.get('answer', '').strip().lower()
        new_pw = request.POST.get('new_password', '')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, 'core/forgot.html', {'error': 'Username haipatikani.'})

        if answer != 'helen':
            return render(request, 'core/forgot.html', {'error': 'Jibu si sahihi.'})

        if len(new_pw) < 6:
            return render(request, 'core/forgot.html', {'error': 'Password lazima iwe na herufi 6+.'})

        user.set_password(new_pw)
        user.save()
        log_activity(user, 'Password imebadilishwa (forgot)', username)
        return render(request, 'core/forgot.html', {'success': 'Password mpya imewekwa! Ingia sasa.'})

    return render(request, 'core/forgot.html')


def logout_view(request):
    log_activity(request.user, 'Ameondoka', request.user.get_full_name() or request.user.username)
    logout(request)
    return redirect('login')


@csrf_exempt
def api_login_view(request):
    if request.method == 'OPTIONS':
        return JsonResponse({'ok': True})
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'ok': False, 'error': 'Invalid data'}, status=400)

    username = (data.get('username') or '').strip()
    password = data.get('password') or ''
    user = authenticate(request, username=username, password=password)

    if user and user.is_active:
        login(request, user)
        log_activity(user, 'Ameingia', f'{user.get_full_name() or user.username} ameingia (e-menu)')
        return JsonResponse({
            'ok': True,
            'username': user.username,
            'role': user.role,
            'name': user.get_full_name() or user.username,
        })

    return JsonResponse({'ok': False, 'error': 'Username au password si sahihi.'}, status=401)


@csrf_exempt
def api_forgot_view(request):
    if request.method == 'OPTIONS':
        return JsonResponse({'ok': True})
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'ok': False, 'error': 'Invalid data'}, status=400)

    username = (data.get('username') or '').strip()
    answer = (data.get('answer') or '').strip().lower()
    new_pw = data.get('new_password') or ''

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Username haipatikani.'}, status=404)

    if answer != 'helen':
        return JsonResponse({'ok': False, 'error': 'Jibu si sahihi.'}, status=400)

    if len(new_pw) < 6:
        return JsonResponse({'ok': False, 'error': 'Password lazima iwe na herufi 6+.'}, status=400)

    user.set_password(new_pw)
    user.save()
    log_activity(user, 'Password imebadilishwa (forgot)', username)
    return JsonResponse({'ok': True, 'message': 'Password mpya imewekwa! Ingia sasa.'})


# ========== ADMIN PANEL ==========

@login_required
@never_cache
def admin_dashboard(request):
    today = date.today()
    foods = Food.objects.filter(is_active=True)
    orders = Order.objects.all()
    today_orders = orders.filter(date=today)

    def rev(qs):
        return qs.aggregate(s=Sum('total'))['s'] or 0

    def growth(cur, prev):
        if prev <= 0:
            return 0
        return round((cur - prev) / prev * 100)

    paid = orders.filter(payment_status='paid')

    revenue_series = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_orders = orders.filter(date=day)
        revenue_series.append({
            'label': day.strftime('%d %b'),
            'revenue': rev(day_orders),
            'count': day_orders.count(),
        })

    yesterday = today - timedelta(days=1)
    today_rev = rev(today_orders)
    yesterday_rev = rev(orders.filter(date=yesterday))

    start_of_week = today - timedelta(days=today.weekday())
    prev_week_end = start_of_week - timedelta(days=1)
    prev_week_start = prev_week_end - timedelta(days=6)
    week_rev = rev(orders.filter(date__gte=start_of_week))
    prev_week_rev = rev(orders.filter(date__gte=prev_week_start, date__lte=prev_week_end))
    week_orders = orders.filter(date__gte=start_of_week).count()

    start_of_month = today.replace(day=1)
    prev_month_end = start_of_month - timedelta(days=1)
    prev_month_start = prev_month_end.replace(day=1)
    month_rev = rev(orders.filter(date__gte=start_of_month))
    prev_month_rev = rev(orders.filter(date__gte=prev_month_start, date__lte=prev_month_end))
    month_orders = orders.filter(date__gte=start_of_month).count()

    year_rev = rev(orders.filter(date__year=today.year))
    prev_year_rev = rev(orders.filter(date__year=today.year - 1))
    year_orders = orders.filter(date__year=today.year).count()

    sw_months = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Ago', 'Sep', 'Okt', 'Nov', 'Des']
    month_series = []
    index = today.year * 12 + (today.month - 1)
    for i in range(index - 7, index + 1):
        m = i % 12 + 1
        mo_orders = orders.filter(date__year=i // 12, date__month=m)
        month_series.append({
            'label': sw_months[m - 1] + (f" '{str(i // 12)[2:]}" if (i // 12) != today.year else ''),
            'revenue': rev(mo_orders),
            'count': mo_orders.count(),
        })
    graph_max = max([s['revenue'] for s in month_series] or [1])
    if graph_max <= 0:
        graph_max = 1

    avg_order = 0
    if orders.count() > 0:
        avg_order = (orders.aggregate(s=Sum('total'))['s'] or 0) // orders.count()

    max_rev = max([r['revenue'] for r in revenue_series] or [0])
    if max_rev <= 0:
        max_rev = 1

    prev_prev_start = (prev_month_start - timedelta(days=1)).replace(day=1)
    pm_orders = orders.filter(date__gte=prev_month_start, date__lte=prev_month_end)
    ppm_orders = orders.filter(date__gte=prev_prev_start, date__lte=prev_month_start - timedelta(days=1))
    prev_month_report = {
        'month': prev_month_end.strftime('%B %Y'),
        'revenue': rev(pm_orders),
        'orders': pm_orders.count(),
        'customers': pm_orders.values('phone').distinct().count(),
        'avg_order': (rev(pm_orders) // pm_orders.count()) if pm_orders.count() else 0,
        'growth': growth(rev(pm_orders), rev(ppm_orders)),
    }

    stats = {
        'total_foods': foods.count(),
        'total_orders': orders.count(),
        'today_orders': today_orders.count(),
        'total_revenue': orders.aggregate(s=Sum('total'))['s'] or 0,
        'today_revenue': today_rev,
        'today_orders_count': today_orders.count(),
        'today_growth': growth(today_rev, yesterday_rev),
        'week_rev': week_rev, 'week_orders': week_orders, 'week_growth': growth(week_rev, prev_week_rev),
        'month_rev': month_rev, 'month_orders': month_orders, 'month_growth': growth(month_rev, prev_month_rev),
        'year_rev': year_rev, 'year_orders': year_orders, 'year_growth': growth(year_rev, prev_year_rev),
        'paid_revenue': rev(paid),
        'unpaid_count': orders.filter(payment_status='unpaid').count(),
        'avg_order': avg_order,
        'total_customers': Order.objects.values('phone').distinct().count(),
        'today_customers_count': today_orders.values('phone').distinct().count(),
        'pending_count': orders.filter(status='new').count(),
        'revenue_series': revenue_series,
        'max_rev': max_rev,
        'month_series': month_series,
        'graph_max': graph_max,
        'graph_json': json.dumps(month_series),
        'prev_month_report': prev_month_report,
        'day_chart_json': json.dumps(_report_build('day')['buckets']),
        'week_chart_json': json.dumps(_report_build('week')['buckets']),
        'month_chart_json': json.dumps(_report_build('month')['buckets']),
        'year_chart_json': json.dumps(_report_build('year')['buckets']),
    }

    recent_orders = orders[:5]
    today_customers = today_orders[:5]
    notifications = Notification.objects.all()[:20]
    unread_notifs = Notification.objects.filter(is_read=False).count()

    context = {**stats, 'recent_orders': recent_orders, 'today_customers': today_customers,
               'notifications': notifications, 'unread_notifs': unread_notifs}
    return render(request, 'core/dashboard.html', context)


def _report_build(period, today=None):
    """Bucketed sales series + summary for day / week / month / year."""
    from calendar import monthrange

    today = today or date.today()
    orders = Order.objects.all()

    def rev(qs):
        return qs.aggregate(s=Sum('total'))['s'] or 0

    def growth(cur, prev):
        if prev <= 0:
            return 0
        return round((cur - prev) / prev * 100)

    buckets, title, label, qf = [], '', '', {}
    if period == 'day':
        title, label = 'Ripoti ya Leo', today.isoformat()
        qf = {'date': today}
        tz = timezone.get_current_timezone()
        rows = list(orders.filter(date=today).values_list('created_at', 'total'))
        hours = [{'label': f'{h:02d}:00', 'revenue': 0, 'count': 0} for h in range(24)]
        for ts, total in rows:
            lt = ts.astimezone(tz) if getattr(ts, 'tzinfo', None) else ts
            hours[lt.hour]['revenue'] += total or 0
            hours[lt.hour]['count'] += 1
        now_h = timezone.localtime().hour
        buckets = [b for i, b in enumerate(hours) if i <= now_h]
        prev = rev(orders.filter(date=today - timedelta(days=1)))
    elif period == 'week':
        monday = today - timedelta(days=today.weekday())
        title, label = 'Ripoti ya Wiki', f'{monday.isoformat()} - {today.isoformat()}'
        qf = {'date__gte': monday, 'date__lte': today}
        dnam = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i in range(7):
            dd = monday + timedelta(days=i)
            if dd > today:
                break
            qs = orders.filter(date=dd)
            buckets.append({'label': f'{dnam[i]} {dd.day}', 'revenue': rev(qs), 'count': qs.count()})
        prev = rev(orders.filter(date__gte=monday - timedelta(days=7), date__lt=monday))
    elif period == 'month':
        title, label = 'Ripoti ya Mwezi Huu', today.strftime('%B %Y')
        qf = {'date__year': today.year, 'date__month': today.month}
        for dd in range(1, today.day + 1):
            qs = orders.filter(date=today.replace(day=dd))
            buckets.append({'label': str(dd), 'revenue': rev(qs), 'count': qs.count()})
        sm = today.replace(day=1)
        pm_end = sm - timedelta(days=1)
        prev = rev(orders.filter(date__gte=pm_end.replace(day=1), date__lte=pm_end))
    elif period == 'year':
        title, label = 'Ripoti ya Mwaka Huu', str(today.year)
        qf = {'date__year': today.year}
        mon = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Ago', 'Sep', 'Okt', 'Nov', 'Des']
        for m in range(1, 13):
            qs = orders.filter(date__year=today.year, date__month=m)
            buckets.append({'label': mon[m - 1], 'revenue': rev(qs), 'count': qs.count()})
        prev = rev(orders.filter(date__year=today.year - 1))

    current = orders.filter(**qf)
    total_revenue = rev(current) or sum(b['revenue'] for b in buckets)
    return {
        'title': title,
        'period_label': label,
        'buckets': buckets,
        'total_revenue': total_revenue,
        'total_orders': current.count(),
        'total_customers': current.values('phone').distinct().count(),
        'growth': growth(total_revenue, prev),
    }


# ========== ORDERS ==========

@login_required
@never_cache
def orders_view(request):
    orders = Order.objects.all()
    status_filter = request.GET.get('status', 'all')
    search = request.GET.get('q', '').strip()

    if status_filter == 'new':
        orders = orders.filter(status='new')
    elif status_filter == 'confirmed':
        orders = orders.filter(status='confirmed')
    elif status_filter == 'paid':
        orders = orders.filter(payment_status='paid')
    elif status_filter == 'unpaid':
        orders = orders.filter(payment_status='unpaid')

    if search:
        orders = orders.filter(
            Q(order_num__icontains=search) | Q(name__icontains=search) | Q(phone__icontains=search)
        )

    notifications = Notification.objects.all()[:20]
    unread_notifs = Notification.objects.filter(is_read=False).count()

    return render(request, 'core/orders.html', {
        'orders': orders, 'status_filter': status_filter, 'search': search,
        'notifications': notifications, 'unread_notifs': unread_notifs,
    })


@login_required
@require_POST
def order_confirm_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = 'confirmed'
    if not order.handled_by:
        order.handled_by = request.user
    order.save()
    log_activity(request.user, 'Agizo limethibitishwa', f'#{order.order_num} {order.name}')
    return redirect('admin_orders')

@login_required
@require_POST
def order_pay_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.payment_status = 'paid'
    if not order.handled_by:
        order.handled_by = request.user
    order.save()
    push_notification(
        f'Malipo yamerekodiwa! #{order.order_num}',
        f'Mteja: {order.name}\nMalipo yamethibitishwa TSh {order.total:,}'
    )
    log_activity(request.user, 'Malipo yamerekodiwa', f'#{order.order_num} TSh {order.total:,}')
    return redirect('admin_orders')


@login_required
@require_POST
def order_delete_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    log_activity(request.user, 'Agizo limefutwa', f'#{order.order_num} {order.name}')
    order.delete()
    return redirect('admin_orders')


@login_required
def order_detail_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    notifications = Notification.objects.all()[:20]
    unread_notifs = Notification.objects.filter(is_read=False).count()
    return render(request, 'core/order_detail.html', {
        'order': order,
        'notifications': notifications, 'unread_notifs': unread_notifs,
    })


@login_required
@require_POST
def orders_clear_view(request):
    log_activity(request.user, 'Maagizo yote yamefutwa', '')
    Order.objects.all().delete()
    return redirect('admin_orders')


# ========== CUSTOMERS ==========

@login_required
def customers_view(request):
    orders = Order.objects.select_related('handled_by').prefetch_related('items__food')
    cust_filter = request.GET.get('filter', 'all')
    search = request.GET.get('q', '').strip()
    today = date.today()

    if cust_filter == 'today':
        orders = orders.filter(date=today)
    elif cust_filter == 'paid':
        orders = orders.filter(payment_status='paid')
    elif cust_filter == 'unpaid':
        orders = orders.filter(payment_status='unpaid')

    if search:
        orders = orders.filter(
            Q(name__icontains=search) | Q(phone__icontains=search) | Q(email__icontains=search)
        )

    notifications = Notification.objects.all()[:20]
    unread_notifs = Notification.objects.filter(is_read=False).count()

    return render(request, 'core/customers.html', {
        'customers': orders, 'current_filter': cust_filter, 'search': search,
        'notifications': notifications, 'unread_notifs': unread_notifs,
    })


# ========== FOODS ==========

@login_required
def foods_view(request):
    foods = Food.objects.all()
    cat_filter = request.GET.get('cat', 'all')
    search = request.GET.get('q', '').strip()

    if cat_filter != 'all':
        foods = foods.filter(category__slug=cat_filter)
    if search:
        foods = foods.filter(Q(name__icontains=search) | Q(name_sw__icontains=search))

    notifications = Notification.objects.all()[:20]
    unread_notifs = Notification.objects.filter(is_read=False).count()

    return render(request, 'core/foods.html', {
        'foods': foods, 'cat_filter': cat_filter, 'search': search,
        'notifications': notifications, 'unread_notifs': unread_notifs,
    })


@login_required
def food_add_view(request):
    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES)
        if form.is_valid():
            food = form.save()
            log_activity(request.user, 'Chakula kipya', f'{food.name} - TSh {food.price:,}')
            return redirect('admin_foods')
    else:
        form = FoodForm()

    notifications = Notification.objects.all()[:20]
    unread_notifs = Notification.objects.filter(is_read=False).count()

    return render(request, 'core/food_form.html', {
        'form': form, 'editing': False,
        'notifications': notifications, 'unread_notifs': unread_notifs,
    })


@login_required
def food_edit_view(request, pk):
    food = get_object_or_404(Food, pk=pk)
    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            form.save()
            log_activity(request.user, 'Chakula kimebadilishwa', food.name)
            return redirect('admin_foods')
    else:
        form = FoodForm(instance=food)

    notifications = Notification.objects.all()[:20]
    unread_notifs = Notification.objects.filter(is_read=False).count()

    return render(request, 'core/food_form.html', {
        'form': form, 'editing': True, 'food': food,
        'notifications': notifications, 'unread_notifs': unread_notifs,
    })


@login_required
@require_POST
def food_delete_view(request, pk):
    food = get_object_or_404(Food, pk=pk)
    log_activity(request.user, 'Chakula kimefutwa', food.name)
    food.delete()
    return redirect('admin_foods')


# ========== USERS ==========

@login_required
def users_view(request):
    if request.user.role != 'admin':
        return redirect('admin_dashboard')

    users = User.objects.all().order_by('-date_joined')
    notifications = Notification.objects.all()[:20]
    unread_notifs = Notification.objects.filter(is_read=False).count()

    return render(request, 'core/users.html', {
        'users': users,
        'notifications': notifications, 'unread_notifs': unread_notifs,
    })


@login_required
def user_add_view(request):
    if request.user.role != 'admin':
        return redirect('admin_dashboard')

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            log_activity(request.user, 'Mtumiaji kipya', f'{user.username} ({user.get_role_display()})')
            return redirect('admin_users')
    else:
        form = UserForm()

    notifications = Notification.objects.all()[:20]
    unread_notifs = Notification.objects.filter(is_read=False).count()

    return render(request, 'core/user_form.html', {
        'form': form, 'editing': False,
        'notifications': notifications, 'unread_notifs': unread_notifs,
    })


@login_required
def user_edit_view(request, pk):
    if request.user.role != 'admin':
        return redirect('admin_dashboard')

    user_obj = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user_obj)
        if form.is_valid():
            user = form.save(commit=False)
            pw = form.cleaned_data.get('password')
            if pw:
                user.set_password(pw)
            user.save()
            log_activity(request.user, 'Mtumiaji kimebadilishwa', user.username)
            return redirect('admin_users')
    else:
        form = UserForm(instance=user_obj)

    notifications = Notification.objects.all()[:20]
    unread_notifs = Notification.objects.filter(is_read=False).count()

    return render(request, 'core/user_form.html', {
        'form': form, 'editing': True, 'user_obj': user_obj,
        'notifications': notifications, 'unread_notifs': unread_notifs,
    })


@login_required
@require_POST
def user_delete_view(request, pk):
    if request.user.role != 'admin':
        return redirect('admin_dashboard')

    user_obj = get_object_or_404(User, pk=pk)
    if user_obj.username == 'admin':
        return redirect('admin_users')

    log_activity(request.user, 'Mtumiaji umefutwa', user_obj.username)
    user_obj.delete()
    return redirect('admin_users')


# ========== PROFILE ==========

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            log_activity(request.user, 'Profaili imebadilishwa', '')
            return redirect('admin_profile')
    else:
        form = ProfileForm(instance=request.user)

    notifications = Notification.objects.all()[:20]
    unread_notifs = Notification.objects.filter(is_read=False).count()

    return render(request, 'core/profile.html', {
        'form': form,
        'notifications': notifications, 'unread_notifs': unread_notifs,
    })


@login_required
@require_POST
def change_password_view(request):
    form = ChangePasswordForm(request.POST)
    if form.is_valid():
        if not request.user.check_password(form.cleaned_data['old_password']):
            return render(request, 'core/profile.html', {
                'form': ProfileForm(instance=request.user),
                'pw_error': 'Password ya zamani si sahihi.',
                'notifications': Notification.objects.all()[:20],
                'unread_notifs': Notification.objects.filter(is_read=False).count(),
            })
        request.user.set_password(form.cleaned_data['new_password'])
        request.user.save()
        log_activity(request.user, 'Password imebadilishwa', '')
        return redirect('admin_profile')

    return redirect('admin_profile')


# ========== ACTIVITY LOG ==========

@login_required
def activity_view(request):
    if request.user.role != 'admin':
        return redirect('admin_dashboard')

    logs = ActivityLog.objects.all()[:100]
    notifications = Notification.objects.all()[:20]
    unread_notifs = Notification.objects.filter(is_read=False).count()

    return render(request, 'core/activity.html', {
        'logs': logs,
        'notifications': notifications, 'unread_notifs': unread_notifs,
    })


@login_required
@require_POST
def activity_clear_view(request):
    if request.user.role == 'admin':
        ActivityLog.objects.all().delete()
    return redirect('admin_activity')


# ========== COMMENTS ==========

@login_required
def comments_view(request):
    comments = Comment.objects.all()
    order_comments = Comment.objects.filter(order__isnull=False)

    notifications = Notification.objects.all()[:20]
    unread_notifs = Notification.objects.filter(is_read=False).count()

    return render(request, 'core/comments.html', {
        'comments': comments,
        'notifications': notifications, 'unread_notifs': unread_notifs,
    })


@login_required
@require_POST
def comments_clear_view(request):
    Comment.objects.all().delete()
    return redirect('admin_comments')


# ========== EXPENSES ==========

@login_required
@never_cache
def expenses_view(request):
    today = timezone.localdate()
    expenses = Expense.objects.all()
    total_all = expenses.aggregate(s=Sum('amount'))['s'] or 0
    total_today = expenses.filter(date=today).aggregate(s=Sum('amount'))['s'] or 0
    total_month = expenses.filter(date__year=today.year, date__month=today.month).aggregate(s=Sum('amount'))['s'] or 0

    error = ''
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        amount = request.POST.get('amount', '').strip()
        category = request.POST.get('category', 'general')
        note = request.POST.get('note', '').strip()
        if not title or not amount:
            error = 'Tafadhali jaza "Kitu" na "Kiasi".'
        else:
            try:
                amount_i = int(amount)
            except ValueError:
                error = 'Kiasi lazima kiwe namba.'
            else:
                Expense.objects.create(
                    title=title, amount=amount_i, category=category,
                    note=note, created_by=request.user,
                )
                log_activity(request.user, 'Expense imeongezwa', f'{title} - {amount_i}')
                push_notification(
                    'Expense mpya',
                    f'{request.user.get_role_display()} ameandika matumizi "{title}" TZS {amount_i}.',
                )
                clear_caches()
                return redirect('admin_expenses')

    notifications = Notification.objects.all()[:20]
    unread_notifs = Notification.objects.filter(is_read=False).count()

    return render(request, 'core/expenses.html', {
        'expenses': expenses,
        'total_all': total_all, 'total_today': total_today, 'total_month': total_month,
        'error': error,
        'notifications': notifications, 'unread_notifs': unread_notifs,
    })


@login_required
@require_POST
def expense_delete_view(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    log_activity(request.user, 'Expense imefutwa', f'{expense.title} - {expense.amount}')
    expense.delete()
    clear_caches()
    return redirect('admin_expenses')


# ========== WALK-IN ORDER ==========

@login_required
def walkin_order_view(request):
    """Record a walk-in customer order (no phone/M-Pesa payment).

    Lets staff quickly capture: customer name, phone, food type, price and
    payment method. Creates an Order (with an OrderItem when a menu food is
    picked) and pushes a notification that admin & accountant see instantly.
    """
    error = ''
    foods = Food.objects.filter(is_active=True).select_related('category')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        food_id = request.POST.get('food', '').strip()
        food_desc = request.POST.get('food_desc', '').strip()
        qty = request.POST.get('qty', '1').strip()
        price = request.POST.get('price', '').strip()
        payment = request.POST.get('payment', 'cash').strip()
        notes = request.POST.get('notes', '').strip()

        if not name:
            name = 'Mteja'

        price_i = 0
        try:
            price_i = int(price) if price else 0
        except ValueError:
            error = 'Bei (price) lazima iwe namba.'

        if not error:
                qty_i = 1
                try:
                    qty_i = int(qty) if qty else 1
                    if qty_i < 1:
                        qty_i = 1
                except ValueError:
                    qty_i = 1

                food = None
                if food_id:
                    food = Food.objects.filter(pk=food_id).first()
                if (not food) and food_desc:
                    notes = (food_desc + (' | ' + notes if notes else '')).strip()

                total = price_i if price_i > 0 else (food.price * qty_i if food else 0)

                order = Order.objects.create(
                    order_num=generate_order_num(),
                    name=name,
                    phone=phone,
                    table_location='Walk-in',
                    payment_method=payment if payment else 'cash',
                    payment_status='paid',
                    total=total,
                    notes=notes,
                    handled_by=request.user,
                    date=date.today(),
                )

                if food:
                    OrderItem.objects.create(
                        order=order, food=food, quantity=qty_i, price=food.price,
                    )
                    order.total = food.price * qty_i
                    order.save()

                label = food.name if food else (food_desc or 'Mlo')
                push_notification(
                    f'Mteja Walk-in! #{order.order_num}',
                    f'Mteja: {name}\nChakula: {label} x{qty_i}\nBei: TSh {order.total:,}\nMalipo: {order.get_payment_method_display()}'
                )
                log_activity(request.user, 'Agizo la mteja walk-in', f'#{order.order_num} {name} TSh {order.total:,}')
                clear_caches()
                messages.success(request, f'Agizo #{order.order_num} limeandikwa ({name}, TSh {order.total:,}).')
                return redirect('admin_orders')

    notifications = Notification.objects.all()[:20]
    unread_notifs = Notification.objects.filter(is_read=False).count()

    return render(request, 'core/walkin_order.html', {
        'foods': foods,
        'error': error,
        'notifications': notifications, 'unread_notifs': unread_notifs,
    })


# ========== SETTINGS ==========

@login_required
def settings_view(request):
    if request.method == 'POST':
        whatsapp = request.POST.get('whatsapp_number', '')
        from django.conf import settings
        settings.WHATSAPP_NUMBER = whatsapp
        log_activity(request.user, 'Settings zimebadilishwa', f'WhatsApp: {whatsapp}')
        return redirect('admin_settings')

    notifications = Notification.objects.all()[:20]
    unread_notifs = Notification.objects.filter(is_read=False).count()

    return render(request, 'core/settings.html', {
        'notifications': notifications, 'unread_notifs': unread_notifs,
    })


# ========== NOTIFICATIONS API ==========

@login_required
def notifications_api(request):
    notifs = Notification.objects.all()[:30]
    data = [{'id': n.id, 'title': n.title, 'detail': n.detail, 'type': '',
             'read': n.is_read, 'time': n.created_at.strftime('%d %b %H:%M')} for n in notifs]
    return JsonResponse({'notifications': data, 'unread': Notification.objects.filter(is_read=False).count()})


@login_required
@require_POST
def notification_read_view(request, pk):
    notif = get_object_or_404(Notification, pk=pk)
    notif.is_read = True
    notif.save()
    return JsonResponse({'ok': True})


@login_required
@require_POST
def notifications_clear_view(request):
    Notification.objects.filter(is_read=False).update(is_read=True)
    return JsonResponse({'ok': True})


@login_required
@never_cache
def notifications_view(request):
    notifs = Notification.objects.all()
    total = notifs.count()
    unread = notifs.filter(is_read=False).count()
    return render(request, 'core/notifications.html', {
        'notifications': notifs[:80],
        'unread_notifs': unread,
        'total_notifs': total,
    })


@login_required
@require_POST
def notifications_delete_view(request):
    Notification.objects.all().delete()
    log_activity(request.user, 'Notifications zimefutwa', 'All notifications cleared')
    return JsonResponse({'ok': True})


# ========== EXPORT / IMPORT ==========

@login_required
@require_POST
def export_view(request):
    foods = list(Food.objects.all().values())
    orders_data = list(Order.objects.all().values())
    data = json.dumps({'foods': foods, 'orders': orders_data}, default=str, indent=2)
    from django.http import HttpResponse
    response = HttpResponse(data, content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="clocktower-backup-{date.today()}.json"'
    return response


@login_required
@require_POST
def export_report_view(request):
    period = request.POST.get('period', '')
    if period not in ('day', 'week', 'month', 'year'):
        return redirect('admin_dashboard')
    rep = _report_build(period)
    import csv
    from io import StringIO
    buf = StringIO()
    w = csv.writer(buf)
    w.writerow([rep['title'], rep['period_label']])
    w.writerow([])
    w.writerow(['Kipindi', 'Mapato (TSh)', 'Maagizo'])
    for b in rep['buckets']:
        w.writerow([b['label'], b['revenue'], b['count']])
    w.writerow([])
    w.writerow(['Jumla', rep['total_revenue'], rep['total_orders']])
    w.writerow(['Wateja', rep['total_customers'], ''])
    w.writerow(['Ukuaji (%)', rep['growth'], ''])
    from django.http import HttpResponse
    response = HttpResponse(buf.getvalue(), content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="clocktower-report-{period}-{date.today().isoformat()}.csv"'
    return response


@login_required
@require_POST
def reset_data_view(request):
    if request.user.role != 'admin':
        return redirect('admin_dashboard')
    Order.objects.all().delete()
    OrderItem.objects.all().delete()
    Comment.objects.all().delete()
    ActivityLog.objects.all().delete()
    Notification.objects.all().delete()
    log_activity(request.user, 'Data yote imefutwa', 'System reset')
    return redirect('admin_settings')


# ========== PUBLIC VIEWS ==========

def menu_view(request):
    categories = Category.objects.all()
    foods = Food.objects.filter(is_active=True)
    return render(request, 'core/menu.html', {'categories': categories, 'foods': foods})


def place_order_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        table_location = request.POST.get('table_location', '').strip()
        payment = request.POST.get('payment_method', '').strip() or 'cash'
        payment_phone = request.POST.get('payment_phone', '').strip()
        share_bill = request.POST.get('share_bill') == 'on'
        share_payment_method = request.POST.get('share_payment_method', '').strip()
        share_payment_phone = request.POST.get('share_payment_phone', '').strip()
        notes = request.POST.get('notes', '').strip()
        comments_text = request.POST.get('comments', '').strip()

        if not name:
            return render(request, 'core/place_order.html', {
                'error': 'Jina ni lazima.',
                'foods': Food.objects.filter(is_active=True),
            })

        order = Order.objects.create(
            order_num=generate_order_num(),
            name=name, phone=phone, email=email,
            table_location=table_location, payment_method=payment,
            payment_phone=payment_phone,
            share_bill=share_bill,
            share_payment_method=share_payment_method,
            share_payment_phone=share_payment_phone,
            notes=notes, comments=comments_text,
            total=0, date=date.today(),
        )

        total = 0
        for key, val in request.POST.items():
            if key.startswith('food_'):
                food_id = key.replace('food_', '')
                qty = int(val) if val.isdigit() else 0
                if qty > 0:
                    try:
                        food = Food.objects.get(pk=food_id)
                        OrderItem.objects.create(order=order, food=food, quantity=qty, price=food.price)
                        total += food.price * qty
                    except Food.DoesNotExist:
                        pass

        order.total = total
        order.save()

        clear_caches()

        if comments_text:
            Comment.objects.create(name=name, email=email, text=comments_text, order=order)

        items_summary = ', '.join([
            f"{item.food.name} x{item.quantity}" for item in order.items.select_related('food').all()
        ])
        payment_label = order.get_payment_status_display()

        push_notification(
            f'Agizo Jipya! #{order.order_num}',
            f'Mteja: {name}\nBidhaa: {items_summary}\nJumla: TSh {total:,}\nMalipo: {payment_label}'
        )
        log_activity(None, 'Agizo kipya', f'#{order.order_num} {name} TSh {total:,}')

        from .notifications import send_order_notifications
        send_order_notifications(order)

        return render(request, 'core/order_success.html', {'order': order})

    foods = Food.objects.filter(is_active=True)
    return render(request, 'core/place_order.html', {'foods': foods})


@csrf_exempt
def api_order_view(request):
    """JSON API used by the Vue user app to file orders so the admin panel
    receives real-time notifications (with sound)."""
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'POST only'}, status=405)

    try:
        data = json.loads(request.body or b'{}')
    except json.JSONDecodeError:
        return JsonResponse({'ok': False, 'error': 'invalid json'}, status=400)

    name = (data.get('name') or '').strip()
    phone = (data.get('phone') or '').strip()
    if not name:
        return JsonResponse({'ok': False, 'error': 'name required'}, status=400)

    payment = (data.get('payment') or '').strip() or 'mpesa'
    payment_status = 'paid' if data.get('paid') else 'unpaid'

    order = Order.objects.create(
        order_num=generate_order_num(),
        name=name,
        phone=phone,
        email=(data.get('email') or '').strip(),
        table_location=(data.get('table') or '').strip(),
        payment_method=payment,
        payment_phone=(data.get('payment_phone') or '').strip(),
        share_bill=bool(data.get('share_bill')),
        share_payment_method=(data.get('share_payment') or '').strip(),
        share_payment_phone=(data.get('share_phone') or '').strip(),
        notes=(data.get('notes') or '').strip(),
        comments=(data.get('comments') or '').strip(),
        payment_status=payment_status,
        total=0,
        date=date.today(),
    )

    total = 0
    items_list = []
    for item in data.get('items') or []:
        vid = item.get('v_id')
        qty = int(item.get('quantity') or 0)
        if not vid or qty <= 0:
            continue
        food = Food.objects.filter(v_id=vid, is_active=True).first()
        if not food:
            continue
        OrderItem.objects.create(order=order, food=food, quantity=qty, price=food.price)
        total += food.price * qty
        items_list.append(f'{food.name} x{qty}')

    order.total = total
    order.save()

    clear_caches()

    comment_text = (data.get('comments') or '').strip()
    if comment_text:
        Comment.objects.create(name=name, email=(data.get('email') or '').strip(),
                               text=comment_text, order=order)

    items_summary = ', '.join(items_list) or 'Hakuna bidhaa'
    push_notification(
        f'Agizo Jipya! #{order.order_num}',
        f'Mteja: {name}\nBidhaa: {items_summary}\nJumla: TSh {total:,}'
    )
    if payment_status == 'paid':
        push_notification(
            f'Lipa Limepokelewa! #{order.order_num}',
            f'Mteja: {name}\nAmetuma malipo TSh {total:,}'
        )
    log_activity(None, 'Agizo kipya (API)', f'#{order.order_num} {name} TSh {total:,}')

    try:
        from .notifications import send_order_notifications
        send_order_notifications(order)
    except Exception:
        pass

    return JsonResponse({'ok': True, 'order_num': order.order_num, 'total': total})


@never_cache
def api_foods_view(request):
    """Public menu API used by the Vue user app so admin edits (names, prices,
    and especially images) show up on the user-facing site immediately.
    never_cache: browsers/devices must refetch the menu each visit instead of
    showing a stale cached one."""
    foods = Food.objects.filter(v_id__gt=0, is_active=True).select_related('category')
    payload = []
    for f in foods:
        img = f.get_image
        if img and not img.startswith(('http://', 'https://', '/', 'media/', 'photos/')):
            img = 'photos/' + img
        payload.append({
            'id': f.v_id,
            'name': f.name,
            'nameSw': f.name_sw or '',
            'category': f.category.slug if f.category else '',
            'price': f.price,
            'icon': f.icon or '🍽️',
            'img': img,
            'rating': float(f.rating) if f.rating is not None else None,
            'popular': f.popular,
            'desc': f.description or '',
            'descSw': f.description_sw or '',
        })
    return JsonResponse({'foods': payload})


# ========== SPA (Vue storefront) ==========

from pathlib import Path
from django.http import FileResponse
from django.views.static import serve as static_serve


@never_cache
def spa_view(request, path=''):
    """Serve the built Vue storefront from Django so the whole system (storefront,
    login, orders and the /api/ endpoints) lives on one origin. Because the SPA
    uses hash-history routing, any unknown path simply returns index.html."""
    from django.conf import settings
    spa_root = Path(settings.SPA_ROOT)
    if path:
        target = (spa_root / path).resolve()
        if target.is_file() and target.is_relative_to(spa_root.resolve()):
            return static_serve(request, target.name, document_root=str(target.parent))
        return FileResponse(open(spa_root / 'index.html', 'rb'))
    return FileResponse(open(spa_root / 'index.html', 'rb'))
