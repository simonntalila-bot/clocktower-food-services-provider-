from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('forgot/', views.forgot_password_view, name='forgot'),
    path('logout/', views.logout_view, name='logout'),

    # Admin Panel
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/orders/', views.orders_view, name='admin_orders'),
    path('admin-panel/orders/<int:pk>/', views.order_detail_view, name='order_detail'),
    path('admin-panel/orders/<int:pk>/confirm/', views.order_confirm_view, name='order_confirm'),
    path('admin-panel/orders/<int:pk>/pay/', views.order_pay_view, name='order_pay'),
    path('admin-panel/orders/<int:pk>/delete/', views.order_delete_view, name='order_delete'),
    path('admin-panel/orders/clear/', views.orders_clear_view, name='orders_clear'),
    path('admin-panel/customers/', views.customers_view, name='admin_customers'),
    path('admin-panel/foods/', views.foods_view, name='admin_foods'),
    path('admin-panel/foods/add/', views.food_add_view, name='food_add'),
    path('admin-panel/foods/<int:pk>/edit/', views.food_edit_view, name='food_edit'),
    path('admin-panel/foods/<int:pk>/delete/', views.food_delete_view, name='food_delete'),
    path('admin-panel/users/', views.users_view, name='admin_users'),
    path('admin-panel/users/add/', views.user_add_view, name='user_add'),
    path('admin-panel/users/<int:pk>/edit/', views.user_edit_view, name='user_edit'),
    path('admin-panel/users/<int:pk>/delete/', views.user_delete_view, name='user_delete'),
    path('admin-panel/profile/', views.profile_view, name='admin_profile'),
    path('admin-panel/profile/password/', views.change_password_view, name='change_password'),
    path('admin-panel/activity/', views.activity_view, name='admin_activity'),
    path('admin-panel/activity/clear/', views.activity_clear_view, name='activity_clear'),
    path('admin-panel/comments/', views.comments_view, name='admin_comments'),
    path('admin-panel/comments/clear/', views.comments_clear_view, name='comments_clear'),
    path('admin-panel/settings/', views.settings_view, name='admin_settings'),
    path('admin-panel/export/', views.export_view, name='export_data'),
    path('admin-panel/export-report/', views.export_report_view, name='export_report'),
    path('admin-panel/reset/', views.reset_data_view, name='reset_data'),

    # API
    path('api/login/', views.api_login_view, name='api_login'),
    path('api/order/', views.api_order_view, name='api_order'),
    path('api/foods/', views.api_foods_view, name='api_foods'),
    path('api/notifications/', views.notifications_api, name='notifications_api'),
    path('api/notifications/<int:pk>/read/', views.notification_read_view, name='notif_read'),
    path('api/notifications/clear/', views.notifications_clear_view, name='notifs_clear'),
    path('api/notifications/delete/', views.notifications_delete_view, name='notifs_delete'),
    path('admin-panel/notifications/', views.notifications_view, name='admin_notifications'),
    path('admin-panel/expenses/', views.expenses_view, name='admin_expenses'),
    path('admin-panel/expenses/<int:pk>/delete/', views.expense_delete_view, name='expense_delete'),

    # Public
    path('', views.menu_view, name='menu'),
    path('order/', views.place_order_view, name='place_order'),
]
