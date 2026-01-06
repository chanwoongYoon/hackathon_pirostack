from django.db import models
from users.models import Profile

# Create your models here.


class Category(models.Model):
    """질문 카테고리 (세션, 과제 등)"""

    name = models.CharField(max_length=50)
    # 운영진이 관리할 수 있도록 타입 구분
    category_type = models.CharField(
        max_length=20,
        choices=[("session", "세션"), ("assignment", "과제")],
        default="session",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    """질문 모델"""

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="questions"
    )
    author = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, related_name="questions"
    )
    title = models.CharField(max_length=200)
    content = models.TextField()

    # 상태 필드
    is_resolved = models.BooleanField(default=False)  # 해결 여부
    is_anonymous = models.BooleanField(default=True)  # 익명 여부

    # [이서현 의존성] 찜하기 기능 (Many-to-Many)
    scraps = models.ManyToManyField(Profile, related_name="scrapped_questions", blank=True)

    is_faq = models.BooleanField(default=False)
    faq_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Answer(models.Model):
    """답변 모델"""

    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    author = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, related_name="answers"
    )
    content = models.TextField()

    # [이영주] 꼬리질문 (대댓글) 기능을 위한 자기 참조
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )

    is_staff = models.BooleanField(default=False)  # 운영진 답변 여부
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Answer to {self.question.title}"


# TODO: [이서현] FAQ 모델 및 API 구현 (자주 묻는 질문, 꿀팁 등)
