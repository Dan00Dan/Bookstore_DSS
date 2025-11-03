"""
Script seed dữ liệu mẫu cho website bán sách.
Chạy bằng lệnh: python manage.py runscript seed_data
"""
import random
from django.utils.text import slugify
from store.models import Category, Book


def run():
    """Hàm chính để seed dữ liệu."""
    print("🔄 Đang xóa dữ liệu cũ...")
    Book.objects.all().delete()
    Category.objects.all().delete()
    print("✅ Đã xóa dữ liệu cũ thành công!")

    # Tạo 5 Category mẫu
    print("\n📚 Đang tạo danh mục...")
    categories_data = [
        {
            'name': 'Tiểu thuyết',
            'description': 'Các tác phẩm tiểu thuyết hay và nổi tiếng'
        },
        {
            'name': 'Khoa học',
            'description': 'Sách về khoa học và công nghệ'
        },
        {
            'name': 'Công nghệ',
            'description': 'Sách về công nghệ thông tin và lập trình'
        },
        {
            'name': 'Kinh tế',
            'description': 'Sách về kinh tế và quản trị kinh doanh'
        },
        {
            'name': 'Tâm lý học',
            'description': 'Sách về tâm lý học và phát triển bản thân'
        }
    ]

    categories = []
    for cat_data in categories_data:
        category = Category.objects.create(
            name=cat_data['name'],
            slug=slugify(cat_data['name']),
            description=cat_data['description']
        )
        categories.append(category)
        print(f"  ✓ Đã tạo danh mục: {category.name}")

    # Tạo 20 Book mẫu
    print("\n📖 Đang tạo sách mẫu...")
    books_data = [
        {
            'title': 'Nhà Giả Kim',
            'author': 'Paulo Coelho',
            'description': 'Cuốn tiểu thuyết nổi tiếng về hành trình tìm kiếm vận mệnh của một chàng trai trẻ tuổi.'
        },
        {
            'title': 'Đắc Nhân Tâm',
            'author': 'Dale Carnegie',
            'description': 'Cuốn sách kinh điển về nghệ thuật ứng xử và giao tiếp với mọi người.'
        },
        {
            'title': 'Sapiens: Lược Sử Loài Người',
            'author': 'Yuval Noah Harari',
            'description': 'Cuốn sách khám phá lịch sử tiến hóa của loài người từ thời đồ đá đến hiện đại.'
        },
        {
            'title': 'Tôi Tài Giỏi, Bạn Cũng Thế',
            'author': 'Adam Khoo',
            'description': 'Cuốn sách chia sẻ phương pháp học tập hiệu quả và phát triển tư duy.'
        },
        {
            'title': 'Lịch Sử Việt Nam Từ Nguồn Gốc Đến Giữa Thế Kỷ XX',
            'author': 'Lê Thành Khôi',
            'description': 'Tác phẩm toàn diện về lịch sử Việt Nam, từ thời tiền sử đến giữa thế kỷ 20.'
        },
        {
            'title': 'Tuổi Trẻ Đáng Giá Bao Nhiêu',
            'author': 'Rosie Nguyễn',
            'description': 'Cuốn sách truyền cảm hứng cho giới trẻ về cách sống và làm việc hiệu quả.'
        },
        {
            'title': 'Chí Phèo',
            'author': 'Nam Cao',
            'description': 'Tác phẩm văn học kinh điển của nền văn học Việt Nam.'
        },
        {
            'title': 'Tôi Là Ai - Và Nếu Vậy Thì Bao Nhiêu?',
            'author': 'Richard David Precht',
            'description': 'Cuốn sách triết học dễ hiểu về những câu hỏi lớn của nhân loại.'
        },
        {
            'title': 'Dế Mèn Phiêu Lưu Ký',
            'author': 'Tô Hoài',
            'description': 'Tác phẩm văn học thiếu nhi kinh điển của Việt Nam.'
        },
        {
            'title': 'Khởi Nghiệp Tinh Gọn',
            'author': 'Eric Ries',
            'description': 'Cuốn sách về phương pháp khởi nghiệp hiện đại, áp dụng nguyên lý Lean Startup.'
        },
        {
            'title': 'Python Cơ Bản',
            'author': 'Nguyễn Văn A',
            'description': 'Cuốn sách hướng dẫn lập trình Python từ cơ bản đến nâng cao.'
        },
        {
            'title': 'JavaScript Toàn Tập',
            'author': 'Trần Thị B',
            'description': 'Tài liệu đầy đủ về JavaScript và các framework hiện đại.'
        },
        {
            'title': 'Kinh Tế Học Vi Mô',
            'author': 'GS. Nguyễn Văn C',
            'description': 'Giáo trình kinh tế học vi mô dành cho sinh viên đại học.'
        },
        {
            'title': 'Quản Trị Doanh Nghiệp',
            'author': 'Michael Porter',
            'description': 'Cuốn sách về chiến lược quản trị và phát triển doanh nghiệp.'
        },
        {
            'title': 'Tâm Lý Học Đám Đông',
            'author': 'Gustave Le Bon',
            'description': 'Nghiên cứu về hành vi và tâm lý của đám đông trong xã hội.'
        },
        {
            'title': 'Suy Nghĩ Nhanh Và Chậm',
            'author': 'Daniel Kahneman',
            'description': 'Cuốn sách về hai hệ thống tư duy của con người.'
        },
        {
            'title': 'Người Trong Bao',
            'author': 'Anton Chekhov',
            'description': 'Truyện ngắn kinh điển của văn học Nga về sự cô độc và sợ hãi.'
        },
        {
            'title': 'Django Web Development',
            'author': 'John Smith',
            'description': 'Hướng dẫn xây dựng ứng dụng web với Django framework.'
        },
        {
            'title': 'React Native Cơ Bản',
            'author': 'Lê Văn D',
            'description': 'Cuốn sách hướng dẫn phát triển ứng dụng mobile với React Native.'
        },
        {
            'title': 'Blockchain và Tiền Điện Tử',
            'author': 'Phạm Thị E',
            'description': 'Giải thích về công nghệ blockchain và các ứng dụng của nó.'
        }
    ]

    # URL ảnh placeholder (có thể thay bằng URL thực tế)
    image_urls = [
        'https://via.placeholder.com/400x600/0066CC/FFFFFF?text=Book+Cover',
        'https://via.placeholder.com/400x600/FF6600/FFFFFF?text=Book+Cover',
        'https://via.placeholder.com/400x600/00CC66/FFFFFF?text=Book+Cover',
        'https://via.placeholder.com/400x600/CC0066/FFFFFF?text=Book+Cover',
        'https://via.placeholder.com/400x600/9900FF/FFFFFF?text=Book+Cover',
    ]

    created_count = 0
    for book_data in books_data:
        # Chọn category ngẫu nhiên
        category = random.choice(categories)
        
        # Tạo giá ngẫu nhiên từ 80,000 đến 250,000
        price = random.randint(80000, 250000)
        
        # Tạo stock ngẫu nhiên từ 5 đến 20
        stock = random.randint(5, 20)
        
        # Chọn image URL ngẫu nhiên
        image_url = random.choice(image_urls)

        book = Book.objects.create(
            title=book_data['title'],
            slug=slugify(book_data['title']),
            author=book_data['author'],
            category=category,
            description=book_data['description'],
            price=price,
            stock=stock,
            is_active=True
        )
        
        # Lưu ý: image_url chỉ là placeholder, nếu muốn lưu thực tế cần download ảnh
        # Ở đây chúng ta để trống image vì cần file thực tế
        
        created_count += 1
        print(f"  ✓ Đã tạo sách: {book.title} ({book.author}) - {price:,} đ")

    print(f"\n✅ Đã tạo {created_count} cuốn sách thành công!")
    print(f"✅ Đã tạo {len(categories)} danh mục thành công!")
    print("\n" + "="*50)
    print("✅ Đã tạo dữ liệu mẫu thành công!")
    print("="*50)

