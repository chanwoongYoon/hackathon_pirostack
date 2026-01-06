from django.contrib import admin
from .models import DiscussionPost, DiscussionComment

# Register your models here.
admin.site.register(DiscussionPost)
admin.site.register(DiscussionComment)