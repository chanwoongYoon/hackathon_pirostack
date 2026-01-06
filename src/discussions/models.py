from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
# 게시글 테이블
class DiscussionPost(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='discussion_posts'
    )
    title = models.CharField(max_length=50)
    content = models.TextField()
    link = models.URLField(blank=True,null=True)
    image = models.ImageField(upload_to='discussions/images/',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title    

# 댓글 테이블
class DiscussionComment(models.Model):
    post = models.ForeignKey(
        DiscussionPost,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='discussion_comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Comment by {self.author}"