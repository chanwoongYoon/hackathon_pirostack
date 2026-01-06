from django.contrib import admin
from .models import Category, Question, Answer

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_type', 'created_at']
    list_filter = ['category_type']
    search_fields = ['name']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'is_resolved', 'is_anonymous', 'created_at']
    list_filter = ['is_resolved', 'is_anonymous', 'category']
    search_fields = ['title', 'content']
    date_hierarchy = 'created_at'


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'author', 'is_staff', 'is_anonymous', 'created_at']
    list_filter = ['is_staff', 'is_anonymous']
    search_fields = ['content']
    date_hierarchy = 'created_at'
