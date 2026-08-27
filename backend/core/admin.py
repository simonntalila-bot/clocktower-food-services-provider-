from django.contrib import admin
from .models import User, Category, Food, Order, OrderItem, Notification, Comment, ActivityLog


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'name_display', 'role', 'phone', 'is_active']
    list_filter = ['role', 'is_active']
    search_fields = ['username', 'first_name', 'last_name', 'phone']

    def name_display(self, obj):
        return obj.get_full_name() or obj.username
    name_display.short_description = 'Name'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_sw', 'slug', 'emoji']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_sw', 'category', 'price', 'rating', 'popular', 'is_active']
    list_filter = ['category', 'popular', 'is_active']
    search_fields = ['name', 'name_sw']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['food', 'quantity', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_num', 'name', 'phone', 'total', 'status', 'payment_status', 'date', 'created_at']
    list_filter = ['status', 'payment_status', 'date', 'payment_method']
    search_fields = ['order_num', 'name', 'phone']
    inlines = [OrderItemInline]
    readonly_fields = ['order_num', 'date', 'created_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_read', 'created_at']
    list_filter = ['is_read']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'text', 'order', 'created_at']
    search_fields = ['name', 'text']


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['action', 'detail', 'user', 'created_at']
    list_filter = ['user']
