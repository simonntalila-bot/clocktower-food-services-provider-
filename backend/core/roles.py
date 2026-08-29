ALL_ROLES = ('admin', 'accountant', 'staff', 'receptionist', 'price_manager')

# Map: URL name -> roles allowed to access that page/route.
# Roles NOT listed for a URL name are blocked (HTTP 403) and the link is hidden.
PERMISSIONS = {
    # Main / Core
    'admin_dashboard': ALL_ROLES,
    'admin_orders': ('admin', 'accountant', 'staff', 'receptionist'),
    'order_detail': ('admin', 'accountant', 'staff', 'receptionist'),
    'order_confirm': ('admin', 'staff', 'receptionist'),
    'order_pay': ('admin', 'accountant', 'receptionist'),
    'order_delete': ('admin', 'accountant'),
    'orders_clear': ('admin',),
    'admin_customers': ('admin', 'accountant', 'receptionist'),
    'admin_comments': ('admin', 'receptionist'),
    'comments_clear': ('admin',),
    'admin_notifications': ALL_ROLES,

    # Expenses (visible to every role)
    'admin_expenses': ALL_ROLES,
    'expense_add': ALL_ROLES,
    'expense_edit': ('admin', 'accountant'),
    'expense_delete': ('admin', 'accountant'),

    # Menu / Food
    'admin_foods': ('admin', 'price_manager', 'staff'),
    'food_add': ('admin', 'price_manager'),
    'food_edit': ('admin', 'price_manager'),
    'food_delete': ('admin',),

    # User management (admin only)
    'admin_users': ('admin',),
    'user_add': ('admin',),
    'user_edit': ('admin',),
    'user_delete': ('admin',),

    # Profile / System
    'admin_profile': ALL_ROLES,
    'change_password': ALL_ROLES,
    'admin_activity': ('admin',),
    'activity_clear': ('admin',),
    'admin_settings': ('admin',),
    'export_data': ('admin', 'accountant'),
    'export_report': ('admin', 'accountant'),
    'reset_data': ('admin',),
}


def roles_for(url_name):
    return PERMISSIONS.get(url_name, ('admin',))


def can(user, url_name):
    if user is None or not user.is_authenticated:
        return False
    if not user.is_active:
        return False
    if user.is_superuser:
        return True
    return user.role in roles_for(url_name)


def admin_allowed_processor(request):
    """Context processor: set of URL names the current user may access."""
    user = getattr(request, 'user', None)
    allowed = set()
    if user and user.is_authenticated:
        for url_name in PERMISSIONS:
            if can(user, url_name):
                allowed.add(url_name)
    return {'admin_allowed': allowed}