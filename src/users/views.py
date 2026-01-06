from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Profile
import os
from dotenv import load_dotenv

# Create your views here.


def signUp(request):

    if request.method == "POST":
        role = request.POST.get("role")
        phone_number = request.POST.get("phone_number")
        name = request.POST.get("name")

        if Profile.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "가입된 번호입니다!!")
            return render(request, "signUp.html")

        if role == "Executive":
            is_staff = True
        else:
            is_staff = False

        new_profile = Profile.objects.create(
            role=role,
            name=name,
            phone_number=phone_number,  # 아이디로 취급
            is_staff=is_staff,
        )
        if role == "Executive":
            return redirect("users:signupPass", pk=new_profile.id)
        return redirect("users:login")
        messages.success(request, "로그인 성공!!")
    return render(request, "signUp.html")


def signupPass(request, pk):
    profile = Profile.objects.get(id=pk)
    context = {"profile": profile}
    if request.method == "POST":
        profile.password = request.POST.get("password")
        profile.save()
        return redirect("users:login")
    return render(request, "password_form.html", context)


def login(request):

    load_dotenv()
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        # password = request.POST.get('password')

        # if check_password(password,secret_password) and phone_number==secret_key:#슈퍼 어드민
        #     print('')
        #     return redirect('users:superadmin')

        # if phone_number==secret_key:#슈퍼 어드민
        #     print('iii')
        #     return redirect('users:superadmin')
        try:
            profile = Profile.objects.get(phone_number=phone_number)  # 프로필 객체 id겟
        except Profile.DoesNotExist:
            messages.error(request, "아이디나 비밀번호가 틀렸습니다")
            return redirect("users:login")

        if profile.is_staff:
            return redirect("users:loginPass", pk=profile.id)

        if profile.permission:
            # 일반 사용자 세션 저장
            request.session["user_id"] = profile.id
            request.session["is_staff"] = False
            request.session["phone_number"] = profile.phone_number
            request.session["name"] = profile.name
            return redirect("questions:list")
        else:
            messages.error(request, "계정 승인을 기다려주세요")
            redirect("users:login")
    return render(request, "login.html")


def loginPass(request, pk):
    profile = Profile.objects.get(id=pk)
    context = {"profile": profile}
    if request.method == "POST":
        print(request.POST.get("password"))
        if profile.password == request.POST.get("password"):
            # 세션에 사용자 정보 저장
            request.session['user_role'] = profile.role
            request.session['user_id'] = profile.id
            request.session['is_staff'] = profile.is_staff
            request.session['phone_number'] = profile.phone_number
            request.session['name'] = profile.name
            # 운영진은 staff 대시보드로 이동
            if profile.is_staff:
                return redirect("questions:staff_unanswered")
            else:
                return redirect("questions:list")
    return render(request, "password_form.html", context)


def superadmin(request):
    if request.method == "POST":
        selected_id = request.POST.get("admit_btn")
        person = Profile.objects.get(id=selected_id)
        person.permission = True
        person.save()

    people = Profile.objects.all()
    context = {"people": people}
    return render(request, "superadmin.html", context)


def logout_view(request):
    """로그아웃 - 세션 정보 삭제"""
    request.session.flush()
    return redirect("users:login")
