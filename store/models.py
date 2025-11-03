from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Tên danh mục')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    description = models.TextField(blank=True, verbose_name='Mô tả')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')

    class Meta:
        verbose_name = 'Danh mục'
        verbose_name_plural = 'Danh mục'
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name='Tên sách')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    author = models.CharField(max_length=100, verbose_name='Tác giả')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books', verbose_name='Danh mục')
    description = models.TextField(verbose_name='Mô tả')
    price = models.DecimalField(max_digits=10, decimal_places=0, validators=[MinValueValidator(0)], verbose_name='Giá')
    image = models.ImageField(upload_to='books/', blank=True, null=True, verbose_name='Hình ảnh')
    stock = models.IntegerField(validators=[MinValueValidator(0)], default=0, verbose_name='Số lượng')
    is_active = models.BooleanField(default=True, verbose_name='Kích hoạt')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')

    class Meta:
        verbose_name = 'Sách'
        verbose_name_plural = 'Sách'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def get_average_rating(self):
        """Tính điểm đánh giá trung bình của sách."""
        avg_rating = self.reviews.aggregate(Avg('rating'))['rating__avg']
        if avg_rating:
            return round(avg_rating, 1)
        return 0
    
    def get_review_count(self):
        """Đếm tổng số đánh giá."""
        return self.reviews.count()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Người dùng')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Số điện thoại')
    address = models.TextField(blank=True, verbose_name='Địa chỉ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')

    class Meta:
        verbose_name = 'Hồ sơ'
        verbose_name_plural = 'Hồ sơ'

    def __str__(self):
        return f'Hồ sơ của {self.user.username}'


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items', verbose_name='Người dùng')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Sách')
    quantity = models.IntegerField(validators=[MinValueValidator(1)], default=1, verbose_name='Số lượng')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')

    class Meta:
        verbose_name = 'Giỏ hàng'
        verbose_name_plural = 'Giỏ hàng'
        unique_together = ['user', 'book']

    def __str__(self):
        return f'{self.user.username} - {self.book.title}'

    def get_total_price(self):
        return self.quantity * self.book.price


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Đang xử lý'),
        ('completed', 'Đã giao'),
        ('cancelled', 'Hủy'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cod', 'Thanh toán khi nhận hàng'),
        ('bank', 'Chuyển khoản ngân hàng'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='Người dùng')
    full_name = models.CharField(max_length=100, verbose_name='Họ và tên')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Số điện thoại')
    address = models.TextField(verbose_name='Địa chỉ')
    total_price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Tổng tiền')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default='cod', verbose_name='Phương thức thanh toán')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Trạng thái')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')

    class Meta:
        verbose_name = 'Đơn hàng'
        verbose_name_plural = 'Đơn hàng'
        ordering = ['-created_at']

    def __str__(self):
        return f'Đơn hàng #{self.id} - {self.user.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Đơn hàng')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Sách')
    quantity = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='Số lượng')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Giá')

    class Meta:
        verbose_name = 'Chi tiết đơn hàng'
        verbose_name_plural = 'Chi tiết đơn hàng'

    def __str__(self):
        return f'{self.order.id} - {self.book.title}'

    def get_total_price(self):
        return self.quantity * self.price


class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 sao'),
        (2, '2 sao'),
        (3, '3 sao'),
        (4, '4 sao'),
        (5, '5 sao'),
    ]
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews', verbose_name='Sách')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name='Người dùng')
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Đánh giá'
    )
    comment = models.TextField(verbose_name='Bình luận')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    
    class Meta:
        verbose_name = 'Đánh giá'
        verbose_name_plural = 'Đánh giá'
        ordering = ['-created_at']
        unique_together = ['book', 'user']  # Mỗi user chỉ đánh giá 1 lần cho mỗi sách
    
    def __str__(self):
        return f'{self.user.username} - {self.book.title} - {self.rating} sao'

