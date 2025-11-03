from django.contrib import admin
from .models import Category, Book, CartItem, Order, OrderItem, Profile, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'price', 'stock', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'author']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'quantity', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'book__title']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['get_total_price_display']
    
    def get_total_price_display(self, obj):
        if obj.pk:
            return f"{obj.get_total_price():,.0f} đ"
        return "-"
    get_total_price_display.short_description = 'Thành tiền'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'payment_method', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['user__username', 'id']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]
    actions = ['mark_as_completed']
    
    fieldsets = (
        ('Thông tin người đặt', {
            'fields': ('user', 'full_name', 'email', 'phone', 'address')
        }),
        ('Thông tin đơn hàng', {
            'fields': ('total_price', 'payment_method', 'status', 'created_at', 'updated_at')
        }),
    )
    
    def mark_as_completed(self, request, queryset):
        """Action để đánh dấu các đơn hàng được chọn là hoàn tất."""
        updated = queryset.update(status='completed')
        self.message_user(
            request,
            f'Đã đánh dấu {updated} đơn hàng là hoàn tất thành công.',
            level='SUCCESS'
        )
    mark_as_completed.short_description = 'Đánh dấu là hoàn tất'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'book', 'quantity', 'price', 'get_total_price_display']
    list_filter = ['order__created_at']
    search_fields = ['order__id', 'book__title']
    
    def get_total_price_display(self, obj):
        return f"{obj.get_total_price():,.0f} đ"
    get_total_price_display.short_description = 'Thành tiền'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'created_at']
    search_fields = ['user__username', 'phone']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['book__title', 'user__username', 'comment']
    readonly_fields = ['created_at', 'updated_at']

