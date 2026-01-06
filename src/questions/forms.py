from django import forms
from .models import Question, Answer, Category


class QuestionForm(forms.ModelForm):
    """질문 작성 폼"""

    class Meta:
        model = Question
        fields = ['category', 'title', 'content']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-control',
                'required': True,
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '질문 제목을 입력하세요',
                'required': True,
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': '질문 내용을 입력하세요',
                'required': True,
            }),
        }
        labels = {
            'category': '카테고리',
            'title': '제목',
            'content': '내용',
        }


class AnswerForm(forms.ModelForm):
    """답변 작성 폼"""

    class Meta:
        model = Answer
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '답변을 입력하세요',
                'required': True,
            }),
        }
        labels = {
            'content': '답변 내용',
        }
