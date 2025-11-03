from django.urls import path
from . import views, views_admin

urlpatterns = [
    path('', views.index, name='index'),
    path('book/<slug:slug>/', views.book_detail, name='book_detail'),

    # --- Giỏ hàng & đơn hàng ---
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:cart_item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('checkout/', views.checkout, name='checkout'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
    path('order/history/', views.order_history, name='order_history'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),

    # --- Tài khoản ---
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # --- Trang quản trị tùy chỉnh ---
    path('manage/dashboard/', views_admin.dashboard, name='dashboard'),

    path('manage/books/', views_admin.admin_books, name='admin_books'),
    path('manage/books/add/', views_admin.add_book, name='add_book'),
    path('manage/books/edit/<int:pk>/', views_admin.edit_book, name='edit_book'),
    path('manage/books/delete/<int:pk>/', views_admin.delete_book, name='delete_book'),

    path('manage/categories/', views_admin.admin_categories, name='admin_categories'),
    path('manage/categories/add/', views_admin.add_category, name='add_category'),
    path('manage/categories/edit/<int:pk>/', views_admin.edit_category, name='edit_category'),
    path('manage/categories/delete/<int:pk>/', views_admin.delete_category, name='delete_category'),

    path('manage/orders/', views_admin.admin_orders, name='admin_orders'),
    path('manage/orders/<int:pk>/approve/', views_admin.approve_order, name='approve_order'),
    path('manage/orders/<int:pk>/delete/', views_admin.delete_order, name='delete_order'),


]
