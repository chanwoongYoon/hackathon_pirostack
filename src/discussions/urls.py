from django.urls import path
from . import views

app_name = 'discussions'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:post_id>/',views.post_detail,name='post_detail'),
    path('create/',views.post_create,name='post_create'),
    path('<int:post_id>/comments/create/',views.comment_create,name='comment_create'),
    path('<int:post_id>/edit/',views.post_edit,name='post_edit'),
    path('<int:post_id>/delete/',views.post_delete,name='post_delete'),
    path('comments/<int:comment_id>/delete/',views.comment_delete,name='comment_delete'),
    path('comments/<int:comment_id>/edit/',views.comment_edit,name='comment_edit'),
]