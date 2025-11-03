# Website Bán Sách - Django

Website bán sách hoàn chỉnh được xây dựng bằng Django với đầy đủ các chức năng: hiển thị danh sách sách, chi tiết sách, giỏ hàng, thanh toán, đăng ký/đăng nhập người dùng, và quản lý đơn hàng.

## Tính năng

- ✅ Trang chủ: Danh sách sách với tìm kiếm và lọc theo danh mục
- ✅ Chi tiết sách: Xem thông tin chi tiết và thêm vào giỏ hàng
- ✅ Giỏ hàng: Xem, sửa, xóa sản phẩm, tính tổng tiền
- ✅ Thanh toán: Nhập thông tin, lưu đơn hàng
- ✅ Đăng ký/Đăng nhập/Đăng xuất người dùng
- ✅ Lịch sử đơn hàng: Xem các đơn hàng đã đặt
- ✅ Quản lý đơn hàng với trạng thái (Đang xử lý, Đã giao, Hủy)
- ✅ Trang Admin: Quản lý sách, danh mục, đơn hàng và người dùng
- ✅ Flash messages (thông báo) cho các hành động
- ✅ Giao diện đẹp với Bootstrap 5
- ✅ 100% tiếng Việt

## Cấu trúc Project

```
bookstore/
├── manage.py
├── bookstore/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── store/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   ├── context_processors.py
│   ├── management/
│   │   └── commands/
│   │       └── seed_data.py
│   ├── templates/
│   │   └── store/
│   │       ├── base.html
│   │       ├── index.html
│   │       ├── book_detail.html
│   │       ├── cart.html
│   │       ├── checkout.html
│   │       ├── order_success.html
│   │       ├── order_history.html
│   │       ├── order_detail.html
│   │       ├── login.html
│   │       └── register.html
│   └── static/
│       └── store/
│           └── css/
│               └── style.css
├── requirements.txt
└── README.md
```

## Models

- **Category**: Danh mục sách
- **Book**: Thông tin sách
- **Profile**: Mở rộng thông tin User
- **CartItem**: Sản phẩm trong giỏ hàng
- **Order**: Đơn hàng
- **OrderItem**: Chi tiết đơn hàng

## Cài đặt và Chạy

### 1. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 2. Tạo migrations và migrate database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Tạo superuser (tài khoản admin)

```bash
python manage.py createsuperuser
```

Nhập thông tin:
- Username
- Email (tùy chọn)
- Password

### 4. Seed dữ liệu mẫu (5-10 quyển sách)

```bash
python manage.py seed_data
```

### 5. Chạy server

```bash
python manage.py runserver
```

### 6. Truy cập website

- Website: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Sử dụng

### Người dùng

1. **Đăng ký tài khoản**: Click "Đăng ký" ở menu trên
2. **Đăng nhập**: Click "Đăng nhập" và nhập thông tin
3. **Xem sách**: Browse danh sách sách ở trang chủ, có thể tìm kiếm hoặc lọc theo danh mục
4. **Xem chi tiết**: Click vào sách để xem thông tin chi tiết
5. **Thêm vào giỏ**: Click "Thêm vào giỏ hàng" (cần đăng nhập)
6. **Giỏ hàng**: Xem giỏ hàng, cập nhật số lượng hoặc xóa sản phẩm
7. **Thanh toán**: Điền thông tin giao hàng và xác nhận đặt hàng
8. **Xem đơn hàng**: Xem lịch sử đơn hàng và chi tiết từng đơn

### Admin

1. Đăng nhập vào http://127.0.0.1:8000/admin/ với tài khoản superuser
2. Quản lý:
   - **Danh mục**: Thêm/sửa/xóa danh mục sách
   - **Sách**: Thêm/sửa/xóa sách, upload hình ảnh
   - **Đơn hàng**: Xem và cập nhật trạng thái đơn hàng
   - **Người dùng**: Quản lý người dùng
   - **Giỏ hàng**: Xem các sản phẩm trong giỏ hàng của người dùng

## Công nghệ sử dụng

- **Backend**: Django 4.2.7
- **Database**: SQLite
- **Frontend**: Bootstrap 5.3.0
- **Icons**: Bootstrap Icons
- **Image Processing**: Pillow

## Lưu ý

- Database SQLite sẽ được tạo tự động khi chạy migrate
- Hình ảnh sách sẽ được lưu trong thư mục `media/books/`
- Static files sẽ được collect vào `staticfiles/` khi deploy production
- Để chạy trong production, cần:
  - Thay đổi `DEBUG = False` trong settings.py
  - Cập nhật `SECRET_KEY`
  - Cấu hình `ALLOWED_HOSTS`
  - Sử dụng database production (PostgreSQL, MySQL, etc.)
  - Cấu hình static files và media files phù hợp

## Tác giả

Website bán sách Django - Dự án học tập

