from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count
import random
from django.core.paginator import Paginator
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.forms import ModelForm  
from django.contrib.auth import logout
import json
from datetime import datetime, timedelta
from .models import Book, Category, CartItem, Order, OrderItem, Profile, Review
from .forms import UserRegistrationForm, CheckoutForm, ReviewForm


def index(request):
    search_query = request.GET.get('search', '')
    category_slug = request.GET.get('category', '')
    
    books = Book.objects.filter(is_active=True)
    
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if category_slug:
        books = books.filter(category__slug=category_slug)
    
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'books': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_slug,
    }
    return render(request, 'store/index.html', context)


def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug, is_active=True)
    reviews = book.reviews.all()
    
    # Kiểm tra xem user đã đánh giá chưa
    user_review = None
    can_review = False
    if request.user.is_authenticated:
        try:
            user_review = Review.objects.get(book=book, user=request.user)
        except Review.DoesNotExist:
            can_review = True
    
    # Xử lý form đánh giá
    if request.method == 'POST' and request.user.is_authenticated:
        # Kiểm tra user đã đánh giá chưa
        if not user_review:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.book = book
                review.user = request.user
                review.save()
                messages.success(request, 'Cảm ơn bạn đã đánh giá!')
                return redirect('book_detail', slug=slug)
        else:
            messages.warning(request, 'Bạn đã đánh giá sách này rồi.')
    else:
        form = ReviewForm()
    
    # Tính điểm trung bình
    average_rating = book.get_average_rating()
    review_count = book.get_review_count()
    
    # Convert average_rating to int for template star display
    average_rating_int = int(round(average_rating)) if average_rating > 0 else 0
    
    # Gợi ý sách tương tự
    similar_books = Book.objects.filter(
        is_active=True
    ).exclude(id=book.id)
    
    # Ưu tiên: sách cùng tác giả hoặc cùng category
    books_by_author = list(similar_books.filter(author=book.author))
    books_by_category = list(similar_books.filter(category=book.category))
    
    # Kết hợp và loại bỏ trùng lặp bằng cách dùng dict
    recommended_books_dict = {}
    for b in books_by_author + books_by_category:
        recommended_books_dict[b.id] = b
    
    recommended_books = list(recommended_books_dict.values())
    
    # Nếu không đủ 3 cuốn, thêm sách ngẫu nhiên
    if len(recommended_books) < 3:
        remaining_books = list(similar_books.exclude(
            id__in=[b.id for b in recommended_books]
        ))
        if remaining_books:
            random.shuffle(remaining_books)
            needed = 3 - len(recommended_books)
            recommended_books.extend(remaining_books[:needed])
    
    # Giới hạn tối đa 3 cuốn
    recommended_books = recommended_books[:3]
    
    context = {
        'book': book,
        'reviews': reviews,
        'form': form,
        'user_review': user_review,
        'can_review': can_review,
        'average_rating': average_rating,
        'average_rating_int': average_rating_int,
        'review_count': review_count,
        'recommended_books': recommended_books,
    }
    return render(request, 'store/book_detail.html', context)


@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        book=book,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'Đã cập nhật số lượng "{book.title}" trong giỏ hàng.')
    else:
        messages.success(request, f'Đã thêm "{book.title}" vào giỏ hàng.')
    
    return redirect('cart')


@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'store/cart.html', context)


@login_required
def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Đã cập nhật giỏ hàng.')
    else:
        cart_item.delete()
        messages.success(request, 'Đã xóa sản phẩm khỏi giỏ hàng.')
    
    return redirect('cart')


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'Đã xóa sản phẩm khỏi giỏ hàng.')
    return redirect('cart')


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    
    if not cart_items.exists():
        messages.warning(request, 'Giỏ hàng của bạn đang trống.')
        return redirect('cart')
    
    total_price = sum(item.get_total_price() for item in cart_items)
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = total_price
            order.save()
            
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    book=cart_item.book,
                    quantity=cart_item.quantity,
                    price=cart_item.book.price
                )
                # Giảm số lượng sách trong kho
                cart_item.book.stock -= cart_item.quantity
                cart_item.book.save()
            
            cart_items.delete()
            messages.success(request, 'Đặt hàng thành công! Cảm ơn bạn đã mua sắm.')
            return redirect('order_success', order_id=order.id)
    else:
        # Tự động điền thông tin nếu có
        try:
            profile = request.user.profile
            initial_data = {
                'full_name': f'{request.user.first_name} {request.user.last_name}'.strip() or request.user.username,
                'email': request.user.email,
                'phone': profile.phone,
                'address': profile.address,
            }
            form = CheckoutForm(initial=initial_data)
        except Profile.DoesNotExist:
            form = CheckoutForm(initial={
                'full_name': f'{request.user.first_name} {request.user.last_name}'.strip() or request.user.username,
                'email': request.user.email,
            })
    
    context = {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'store/checkout.html', context)


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        'order': order,
    }
    return render(request, 'store/order_success.html', context)


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'store/order_history.html', context)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        'order': order,
    }
    return render(request, 'store/order_detail.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Tạo Profile cho user
            Profile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Tài khoản {username} đã được tạo thành công!')
            login(request, user)
            return redirect('index')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'store/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Chào mừng trở lại, {user.username}!')

            # 🔹 Nếu là admin, chuyển thẳng đến dashboard
            if user.is_staff or user.is_superuser:
                return redirect('dashboard')
            
            # 🔹 Nếu là user thường, về trang chủ
            next_url = request.GET.get('next', None)
            if next_url:
                return redirect(next_url)
            return redirect('index')
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng.')
    
    return render(request, 'store/login.html')

def logout_view(request):
    """Đăng xuất người dùng và quay lại trang chủ."""
    logout(request)
    return redirect('index')



@staff_member_required
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, f'Chào mừng quản trị viên {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Sai tài khoản hoặc không có quyền truy cập quản trị.')
    return render(request, 'store/admin_login.html')

@login_required
def dashboard(request):
    """Trang dashboard chỉ dành cho admin."""
    # Nếu user không phải admin thì chuyển hướng về trang chủ
    if not request.user.is_staff:
        from django.contrib import messages
        messages.warning(request, "Bạn không có quyền truy cập trang quản trị.")
        return redirect("index")

    from django.utils import timezone
    from django.db.models import Sum
    from django.utils.safestring import mark_safe
    import json

    today = timezone.now().date()
    start_of_month = today.replace(day=1)

    from .models import Order, OrderItem

    # Tổng doanh thu hôm nay (chỉ đơn hàng đã hoàn thành)
    today_revenue = (
        Order.objects.filter(status="completed", created_at__date=today)
        .aggregate(total=Sum("total_price"))
        .get("total")
        or 0
    )

    # Tổng doanh thu tháng này
    month_revenue = (
        Order.objects.filter(status="completed", created_at__date__gte=start_of_month)
        .aggregate(total=Sum("total_price"))
        .get("total")
        or 0
    )

    # Top 5 sách bán chạy
    top_books = (
        OrderItem.objects.filter(order__status="completed")
        .values("book__title", "book__author")
        .annotate(total_sold=Sum("quantity"))
        .order_by("-total_sold")[:5]
    )

    chart_labels = [b["book__title"] for b in top_books]
    chart_data = [int(b["total_sold"]) for b in top_books]

    context = {
        "today_revenue": today_revenue,
        "month_revenue": month_revenue,
        "top_books": top_books,
        "chart_labels": mark_safe(json.dumps(chart_labels, ensure_ascii=False)),
        "chart_data": mark_safe(json.dumps(chart_data)),
    }

    # Trả về template dashboard.html
    return render(request, "store/dashboard.html", context)

    
    # --- Form quản lý sách ---
class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'slug', 'author', 'category', 'description', 'price', 'image', 'stock', 'is_active']

# --- Danh sách sách ---
@staff_member_required
def manage_books(request):
    books = Book.objects.all().order_by('-created_at')
    return render(request, 'store/manage_books.html', {'books': books})

# --- Thêm sách ---
@staff_member_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Đã thêm sách mới thành công!')
            return redirect('manage_books')
    else:
        form = BookForm()
    return render(request, 'store/book_form.html', {'form': form, 'title': 'Thêm sách mới'})

# --- Sửa sách ---
@staff_member_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Đã cập nhật thông tin sách.')
            return redirect('manage_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'store/book_form.html', {'form': form, 'title': f'Sửa: {book.title}'})

# --- Xóa sách ---
@staff_member_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    messages.success(request, '🗑️ Đã xóa sách thành công!')
    return redirect('manage_books')

    # Chuẩn bị dữ liệu cho biểu đồ Chart.js
    chart_labels = []
    chart_data = []
    
    for item in top_books:
        chart_labels.append(item['book__title'])
        chart_data.append(int(item['total_sold']))
    
    # Serialize dữ liệu JSON cho JavaScript
    chart_labels_json = mark_safe(json.dumps(chart_labels, ensure_ascii=False))
    chart_data_json = mark_safe(json.dumps(chart_data))
    
    context = {
        'today_revenue': today_revenue,
        'month_revenue': month_revenue,
        'top_books': top_books,
        'chart_labels': chart_labels_json,
        'chart_data': chart_data_json,
    }
    
    return render(request, 'store/dashboard.html', context)

