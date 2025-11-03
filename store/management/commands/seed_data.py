from django.core.management.base import BaseCommand
from store.models import Category, Book


class Command(BaseCommand):
    help = 'Seed dữ liệu mẫu cho cửa hàng sách'

    def handle(self, *args, **options):
        self.stdout.write('Đang tạo dữ liệu mẫu...')

        # Tạo danh mục
        categories_data = [
            {'name': 'Tiểu thuyết', 'slug': 'tieu-thuyet', 'description': 'Các tác phẩm tiểu thuyết hay'},
            {'name': 'Kỹ năng sống', 'slug': 'ky-nang-song', 'description': 'Sách về kỹ năng và phát triển bản thân'},
            {'name': 'Khoa học', 'slug': 'khoa-hoc', 'description': 'Sách khoa học và công nghệ'},
            {'name': 'Lịch sử', 'slug': 'lich-su', 'description': 'Sách về lịch sử Việt Nam và thế giới'},
            {'name': 'Văn học', 'slug': 'van-hoc', 'description': 'Tác phẩm văn học kinh điển'},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories[cat_data['slug']] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'Đã tạo danh mục: {category.name}'))
            else:
                self.stdout.write(f'Danh mục đã tồn tại: {category.name}')

        # Tạo sách
        books_data = [
            {
                'title': 'Nhà Giả Kim',
                'slug': 'nha-gia-kim',
                'author': 'Paulo Coelho',
                'category': categories['tieu-thuyet'],
                'description': 'Cuốn tiểu thuyết nổi tiếng về hành trình tìm kiếm vận mệnh của một chàng trai chăn cừu trẻ tuổi. Câu chuyện đầy cảm hứng về việc theo đuổi giấc mơ và khám phá bản thân.',
                'price': 89000,
                'stock': 50,
            },
            {
                'title': 'Đắc Nhân Tâm',
                'slug': 'dac-nhan-tam',
                'author': 'Dale Carnegie',
                'category': categories['ky-nang-song'],
                'description': 'Cuốn sách kinh điển về nghệ thuật ứng xử và giao tiếp với mọi người. Giúp bạn xây dựng mối quan hệ tốt đẹp và thành công trong cuộc sống.',
                'price': 95000,
                'stock': 80,
            },
            {
                'title': 'Sapiens: Lược Sử Loài Người',
                'slug': 'sapiens-luoc-su-loai-nguoi',
                'author': 'Yuval Noah Harari',
                'category': categories['khoa-hoc'],
                'description': 'Cuốn sách khám phá lịch sử tiến hóa của loài người từ thời đồ đá đến hiện đại. Một góc nhìn mới mẻ và sâu sắc về nhân loại.',
                'price': 185000,
                'stock': 30,
            },
            {
                'title': 'Tôi Tài Giỏi, Bạn Cũng Thế',
                'slug': 'toi-tai-gioi-ban-cung-the',
                'author': 'Adam Khoo',
                'category': categories['ky-nang-song'],
                'description': 'Cuốn sách chia sẻ phương pháp học tập hiệu quả và phát triển tư duy. Giúp bạn đạt được thành công trong học tập và cuộc sống.',
                'price': 120000,
                'stock': 60,
            },
            {
                'title': 'Lịch Sử Việt Nam Từ Nguồn Gốc Đến Giữa Thế Kỷ XX',
                'slug': 'lich-su-viet-nam-tu-nguon-goc-den-giua-the-ky-xx',
                'author': 'Lê Thành Khôi',
                'category': categories['lich-su'],
                'description': 'Tác phẩm toàn diện về lịch sử Việt Nam, từ thời tiền sử đến giữa thế kỷ 20. Một nguồn tài liệu quý giá cho những ai yêu thích lịch sử nước nhà.',
                'price': 250000,
                'stock': 25,
            },
            {
                'title': 'Tuổi Trẻ Đáng Giá Bao Nhiêu',
                'slug': 'tuoi-tre-dang-gia-bao-nhieu',
                'author': 'Rosie Nguyễn',
                'category': categories['ky-nang-song'],
                'description': 'Cuốn sách truyền cảm hứng cho giới trẻ về cách sống và làm việc hiệu quả. Giúp bạn tận dụng tốt nhất quãng thời gian tuổi trẻ của mình.',
                'price': 75000,
                'stock': 70,
            },
            {
                'title': 'Chí Phèo',
                'slug': 'chi-pheo',
                'author': 'Nam Cao',
                'category': categories['van-hoc'],
                'description': 'Tác phẩm văn học kinh điển của nền văn học Việt Nam. Câu chuyện về số phận con người trong xã hội cũ, mang đậm tính nhân văn.',
                'price': 45000,
                'stock': 100,
            },
            {
                'title': 'Tôi Là Ai - Và Nếu Vậy Thì Bao Nhiêu?',
                'slug': 'toi-la-ai-va-neu-vay-thi-bao-nhieu',
                'author': 'Richard David Precht',
                'category': categories['khoa-hoc'],
                'description': 'Cuốn sách triết học dễ hiểu về những câu hỏi lớn của nhân loại. Giúp bạn hiểu hơn về bản thân và thế giới xung quanh.',
                'price': 165000,
                'stock': 40,
            },
            {
                'title': 'Dế Mèn Phiêu Lưu Ký',
                'slug': 'de-men-phieu-luu-ky',
                'author': 'Tô Hoài',
                'category': categories['van-hoc'],
                'description': 'Tác phẩm văn học thiếu nhi kinh điển của Việt Nam. Câu chuyện về chú dế mèn dũng cảm và cuộc phiêu lưu đầy thú vị.',
                'price': 55000,
                'stock': 90,
            },
            {
                'title': 'Khởi Nghiệp Tinh Gọn',
                'slug': 'khoi-nghiep-tinh-gon',
                'author': 'Eric Ries',
                'category': categories['ky-nang-song'],
                'description': 'Cuốn sách về phương pháp khởi nghiệp hiện đại, giúp bạn xây dựng doanh nghiệp thành công với nguồn lực tối thiểu. Áp dụng nguyên lý Lean Startup.',
                'price': 145000,
                'stock': 35,
            },
        ]

        for book_data in books_data:
            book, created = Book.objects.get_or_create(
                slug=book_data['slug'],
                defaults=book_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Đã tạo sách: {book.title}'))
            else:
                self.stdout.write(f'Sách đã tồn tại: {book.title}')

        self.stdout.write(self.style.SUCCESS('\nHoàn thành! Đã tạo dữ liệu mẫu thành công.'))

