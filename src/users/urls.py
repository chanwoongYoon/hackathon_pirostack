from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('superadmin/',views.superadmin,name='superadmin'),
    path('signup/', views.signUp, name='signUp'),
    path('',views.login, name='login'),
    path('signupPass/<int:pk>/',views.signupPass,name='signupPass'),
    path('loginPass/<int:pk>/',views.loginPass,name='loginPass'),
    path('logout/', views.logout_view, name='logout')
]