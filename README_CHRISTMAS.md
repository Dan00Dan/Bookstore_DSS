# Cập nhật giao diện Giáng Sinh - Tiệm sách Urahara 🎄

## Những thay đổi đã thực hiện:

### 1. Đổi thương hiệu
- ✅ Đổi tên từ "Cửa hàng sách" thành **"Tiệm sách Urahara"** trên:
  - Navbar
  - Title (tất cả các trang)
  - Footer
  - Admin site (đã cập nhật trong urls.py)

### 2. Banner Noel
- ✅ Thêm banner Noel ở đầu trang chủ với:
  - Hình ảnh: `static/store/img/banner_noel.jpg`
  - Text: "CHÀO MỪNG BẠN ĐẾN VỚI TIỆM SÁCH URAHARA 🎄"
  - Hiệu ứng glow animation
  - Hiệu ứng tuyết rơi (snow.js)

### 3. Trang đăng nhập mới
- ✅ Form đăng nhập từ Uiverse.io với:
  - Design hiện đại
  - SVG icons
  - Responsive
  - Giữ nguyên logic Django (csrf_token, username, password)
  - Buttons Google và Apple (UI only)

### 4. Rating System mới
- ✅ Thay rating dropdown bằng SVG star radio buttons:
  - Animation khi hover
  - Animation khi chọn
  - Hiệu ứng sáng vàng (--christmas-gold)
  - Responsive

### 5. Theme Giáng Sinh
- ✅ File `christmas.css` với:
  - Màu chủ đạo: đỏ (#C62828), xanh lá (#2E7D32), vàng (#FFD54F)
  - Background tuyết nhẹ cho body
  - Primary button màu đỏ Giáng Sinh
  - Navbar màu đỏ
  - Footer gradient đỏ-xanh
  - Card borders với accent đỏ

### 6. Hiệu ứng tuyết
- ✅ JavaScript (snow.js) tạo 50 snowflakes:
  - Animation rơi tự nhiên
  - Random position và speed
  - Chỉ hiển thị trên banner

## Cấu trúc file mới:

```
store/static/store/
├── css/
│   ├── christmas.css      (Theme Giáng Sinh)
│   ├── login-form.css     (Form đăng nhập)
│   ├── rating.css         (Rating stars)
│   └── style.css          (CSS gốc)
├── js/
│   └── snow.js            (Hiệu ứng tuyết)
└── img/
    └── banner_noel.jpg    (Cần thêm hình ảnh)
```

## Lưu ý:

1. **Hình ảnh banner**: Cần thêm file `banner_noel.jpg` vào thư mục `store/static/store/img/`
   - Nếu không có, banner vẫn hiển thị text và hiệu ứng tuyết
   - Ảnh được ẩn tự động nếu không tồn tại (onerror)

2. **Tất cả các trang đã được cập nhật**:
   - index.html
   - book_detail.html
   - login.html
   - register.html
   - cart.html
   - checkout.html
   - order_history.html
   - order_detail.html
   - order_success.html
   - dashboard.html

3. **Logic Django không thay đổi**:
   - Tất cả form vẫn hoạt động như cũ
   - Chỉ thay đổi giao diện (HTML, CSS, JS)

## Cách test:

1. Chạy server: `python manage.py runserver`
2. Kiểm tra:
   - Banner Noel với hiệu ứng tuyết ở trang chủ
   - Form đăng nhập mới
   - Rating stars với animation
   - Theme màu đỏ/xanh/vàng trên toàn bộ website

## Tùy chỉnh:

- Màu sắc: Sửa các biến CSS trong `christmas.css`:
  ```css
  --christmas-red: #C62828;
  --christmas-green: #2E7D32;
  --christmas-gold: #FFD54F;
  ```

- Số lượng tuyết: Sửa trong `snow.js`:
  ```javascript
  for (let i = 0; i < 50; i++) { // Thay đổi số 50
  ```

