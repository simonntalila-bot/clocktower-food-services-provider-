from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('accountant', 'Accountant / Mhasibu'),
        ('staff', 'Staff / Mfanyakazi'),
        ('receptionist', 'Receptionist / Msaidizi'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')
    phone = models.CharField(max_length=20, blank=True)
    security_answer = models.CharField(max_length=200, blank=True, default='helen')

    groups = models.ManyToManyField('auth.Group', related_name='ctf_users', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='ctf_user_permissions', blank=True)

    class Meta:
        db_table = 'ctf_users'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Category(models.Model):
    name = models.CharField(max_length=50)
    name_sw = models.CharField(max_length=50, blank=True)
    slug = models.SlugField(unique=True)
    emoji = models.CharField(max_length=10, default='🍽️')
    color = models.CharField(max_length=20, default='#ffb84d')

    class Meta:
        db_table = 'ctf_categories'
        verbose_name_plural = 'categories'

    def __str__(self):
        return f"{self.emoji} {self.name}"


class Food(models.Model):
    name = models.CharField(max_length=100)
    name_sw = models.CharField(max_length=100, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='foods')
    price = models.PositiveIntegerField(default=0)
    icon = models.CharField(max_length=10, blank=True, default='')
    description = models.TextField(blank=True)
    description_sw = models.TextField(blank=True)
    image = models.ImageField(upload_to='foods/', blank=True, null=True)
    image_url = models.URLField(blank=True, help_text='Fallback URL if no image uploaded')
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    popular = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    v_id = models.PositiveIntegerField(default=0, db_index=True, help_text='Vue app food id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ctf_foods'
        ordering = ['-popular', '-created_at']

    def __str__(self):
        return f"{self.icon} {self.name}"

    @property
    def get_image(self):
        if self.image:
            return self.image.url
        return self.image_url or ''


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'New / Mpya'),
        ('confirmed', 'Confirmed / Imethibitishwa'),
        ('delivered', 'Delivered / Imefikishwa'),
        ('cancelled', 'Cancelled / Imefutwa'),
    ]
    PAYMENT_STATUS = [
        ('unpaid', 'Unpaid / Haijalipwa'),
        ('paid', 'Paid / Imelipwa'),
    ]
    PAYMENT_METHODS = [
        ('mpesa', 'M-Pesa'),
        ('tigo', 'Tigo Pesa'),
        ('airtel', 'Airtel Money'),
        ('halo', 'Halopesa'),
        ('bank', 'Bank Transfer'),
        ('cash', 'Cash / Taslimu'),
        ('other', 'Nyingine'),
    ]

    order_num = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    table_location = models.CharField(max_length=100, blank=True, verbose_name='Table / Location')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='mpesa')
    payment_phone = models.CharField(max_length=20, blank=True, verbose_name='Payment Phone Number')
    share_bill = models.BooleanField(default=False, verbose_name='Share Bill')
    share_payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, blank=True, verbose_name='Share Payment Method')
    share_payment_phone = models.CharField(max_length=20, blank=True, verbose_name='Share Payment Phone Number')
    notes = models.TextField(blank=True)
    comments = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='unpaid')
    total = models.PositiveIntegerField(default=0)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ctf_orders'
        ordering = ['-created_at']

    def __str__(self):
        return f"#{self.order_num} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.order_num:
            last = Order.objects.order_by('-id').first()
            num = (last.id + 1) if last else 1
            self.order_num = f"CTF-{num:06d}"
        super().save(*args, **kwargs)

    @property
    def items_text(self):
        return ', '.join([str(item) for item in self.items.all()])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'ctf_order_items'

    def __str__(self):
        return f"{self.food.name} x{self.quantity}"

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.food.price
        super().save(*args, **kwargs)

    @property
    def subtotal(self):
        return self.price * self.quantity


class Notification(models.Model):
    title = models.CharField(max_length=200)
    detail = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ctf_notifications'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    text = models.TextField()
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ctf_comments'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name}: {self.text[:50]}"


class ActivityLog(models.Model):
    action = models.CharField(max_length=200)
    detail = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ctf_activity_logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.action} - {self.user}"


class NotificationLog(models.Model):
    TYPE_CHOICES = [
        ('CUSTOMER_EMAIL', 'Customer Email'),
        ('INTERNAL_EMAIL', 'Internal Email'),
        ('WHATSAPP_ADMIN_1', 'WhatsApp Admin 1'),
        ('WHATSAPP_ADMIN_2', 'WhatsApp Admin 2'),
        ('WHATSAPP_RECEPTION', 'WhatsApp Reception'),
    ]
    STATUS_CHOICES = [
        ('SENT', 'Sent'),
        ('FAILED', 'Failed'),
        ('SKIPPED', 'Skipped'),
    ]

    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='notification_logs')
    notification_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    recipient = models.CharField(max_length=200)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ctf_notification_logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.notification_type} -> {self.recipient} [{self.status}]"
