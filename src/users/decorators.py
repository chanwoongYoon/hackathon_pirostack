from django.shortcuts import redirect
from functools import wraps

def staff_required(view_func):
    """운영진만 접근 가능하도록 하는 데코레이터"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # 미들웨어에서 설정한 request.is_staff 또는 세션에서 직접 확인
        is_staff = getattr(request, 'is_staff', False) or request.session.get('is_staff', False)

        if not is_staff:
            # 운영진이 아니면 questions:list로 리다이렉트
            return redirect('questions:list')
        return view_func(request, *args, **kwargs)
    return wrapper
