from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Order, Review
from .models import Book, Category


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length=30, required=False, label='Tên')
    last_name = forms.CharField(max_length=30, required=False, label='Họ')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'username': 'Tên đăng nhập',
            'password1': 'Mật khẩu',
            'password2': 'Xác nhận mật khẩu',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone', 'address', 'payment_method']
        labels = {
            'full_name': 'Họ và tên',
            'email': 'Email',
            'phone': 'Số điện thoại',
            'address': 'Địa chỉ giao hàng',
            'payment_method': 'Phương thức thanh toán',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        labels = {
            'rating': 'Đánh giá',
            'comment': 'Bình luận',
        }
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Nhập bình luận của bạn...'}),
        }

# Form thêm / chỉnh sửa sách
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'price', 'stock', 'category', 'image', 'description', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên sách'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tác giả'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Giá bán'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Số lượng tồn'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Mô tả ngắn'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# Form thêm / chỉnh sửa danh mục
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên danh mục'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'slug (tự sinh nếu để trống)'}),
        }

