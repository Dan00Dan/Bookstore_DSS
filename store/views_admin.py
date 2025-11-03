from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from django.utils.timezone import now
from .models import Book, Category, Order, OrderItem
from .forms import BookForm, CategoryForm


# ✅ Hàm kiểm tra admin
def admin_required(user):
    return user.is_authenticated and user.is_staff


# === DASHBOARD (Trang tổng quan) ===
@login_required
@user_passes_test(admin_required)
def dashboard(request):
    """Trang tổng quan thống kê dành cho admin"""
    today = now().date()

    # Tổng đơn hàng hôm nay và trong tháng
    today_orders = Order.objects.filter(created_at__date=today)
    month_orders = Order.objects.filter(created_at__month=today.month)

    # Doanh thu
    today_revenue = today_orders.filter(status='completed').aggregate(Sum('total_price'))['total_price__sum'] or 0
    month_revenue = month_orders.filter(status='completed').aggregate(Sum('total_price'))['total_price__sum'] or 0

    # Top 5 sách bán chạy nhất
    top_books = (
        OrderItem.objects.filter(order__status='completed')
        .values('book__title', 'book__author')
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')[:5]
    )

    context = {
        'today_revenue': today_revenue,
        'month_revenue': month_revenue,
        'top_books': top_books,
        'chart_labels': [b['book__title'] for b in top_books],
        'chart_data': [b['total_sold'] for b in top_books],
    }
    return render(request, 'store/dashboard.html', context)


# === QUẢN LÝ SÁCH ===
@login_required
@user_passes_test(admin_required)
def admin_books(request):
    books = Book.objects.all().order_by('-id')
    return render(request, 'store/admin_books.html', {'books': books})


@login_required
@user_passes_test(admin_required)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Đã thêm sách thành công!')
            return redirect('admin_books')
    else:
        form = BookForm()
    return render(request, 'store/admin_book_form.html', {'form': form, 'action': 'Thêm'})


@login_required
@user_passes_test(admin_required)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, '✏️ Đã cập nhật sách!')
            return redirect('admin_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'store/admin_book_form.html', {'form': form, 'action': 'Sửa'})


@login_required
@user_passes_test(admin_required)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    messages.warning(request, '🗑️ Đã xóa sách!')
    return redirect('admin_books')


# === QUẢN LÝ DANH MỤC ===
@login_required
@user_passes_test(admin_required)
def admin_categories(request):
    categories = Category.objects.all()
    return render(request, 'store/admin_categories.html', {'categories': categories})


@login_required
@user_passes_test(admin_required)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Đã thêm danh mục!')
            return redirect('admin_categories')
    else:
        form = CategoryForm()
    return render(request, 'store/admin_category_form.html', {'form': form, 'action': 'Thêm'})


@login_required
@user_passes_test(admin_required)
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, '✏️ Đã cập nhật danh mục!')
            return redirect('admin_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'store/admin_category_form.html', {'form': form, 'action': 'Sửa'})


@login_required
@user_passes_test(admin_required)
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.warning(request, '🗑️ Đã xóa danh mục!')
    return redirect('admin_categories')


# === QUẢN LÝ ĐƠN HÀNG ===
@login_required
@user_passes_test(admin_required)
def admin_orders(request):
    """Hiển thị tất cả đơn hàng cho admin duyệt"""
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'store/admin_orders.html', {'orders': orders})


@login_required
@user_passes_test(admin_required)
def approve_order(request, pk):
    """Duyệt đơn hàng (đổi trạng thái sang completed)"""
    order = get_object_or_404(Order, pk=pk)
    order.status = 'completed'
    order.save()
    messages.success(request, f'✅ Đơn hàng #{order.id} đã được duyệt!')
    return redirect('admin_orders')


@login_required
@user_passes_test(admin_required)
def delete_order(request, pk):
    """Xóa đơn hàng"""
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    messages.warning(request, f'🗑️ Đã xóa đơn hàng #{order.id}!')
    return redirect('admin_orders')
