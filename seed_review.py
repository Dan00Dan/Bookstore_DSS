import os
import django
import random
from faker import Faker

# Cấu hình Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import Book, Review

fake = Faker('vi_VN')

def create_fake_users(n=5):
    """Tạo user mẫu nếu chưa có"""
    existing_users = User.objects.count()
    if existing_users >= n:
        print(f"✅ Đã có {existing_users} user, không cần tạo thêm.")
        return list(User.objects.all())

    users = []
    for i in range(n):
        username = f"user{i+1}"
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=f"{username}@example.com",
                password="123456"
            )
            users.append(user)
            print(f"🧑‍💻 Tạo user: {username} / pass: 123456")
    return list(User.objects.all())

def create_fake_reviews(n=30):
    """Tạo review mẫu"""
    books = list(Book.objects.all())
    users = create_fake_users()

    if not books:
        print("⚠️ Chưa có sách trong cơ sở dữ liệu! Hãy seed Book trước.")
        return

    created = 0
    for _ in range(n):
        book = random.choice(books)
        user = random.choice(users)

        # Kiểm tra nếu user đã review sách đó
        if Review.objects.filter(book=book, user=user).exists():
            continue

        rating = random.randint(3, 5)  # ưu tiên đánh giá tốt
        comment = random.choice([
            "Sách rất hay, đáng đọc!",
            "Nội dung hấp dẫn và ý nghĩa.",
            "Cách viết mạch lạc, dễ hiểu.",
            "Mình rất thích cuốn này.",
            "Một cuốn sách tuyệt vời, 5 sao!",
            "Đọc cuốn này giúp mình học được nhiều điều mới."
        ])

        Review.objects.create(
            book=book,
            user=user,
            rating=rating,
            comment=comment
        )
        created += 1
        print(f"✅ {user.username} → {book.title} ({rating}⭐): {comment}")

    print(f"\n🎉 Đã tạo {created} review mẫu thành công!")

if __name__ == "__main__":
    create_fake_reviews()
