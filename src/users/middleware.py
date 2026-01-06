from django.utils.deprecation import MiddlewareMixin
from .models import Profile

class SessionUserMiddleware(MiddlewareMixin):
    """
    세션 기반 사용자 정보를 request.user에 추가하는 미들웨어
    """
    def process_request(self, request):
        user_id = request.session.get('user_id')

        if user_id:
            try:
                profile = Profile.objects.get(id=user_id)
                # request에 사용자 정보 추가
                request.user_profile = profile
                request.is_staff = request.session.get('is_staff', False)
            except Profile.DoesNotExist:
                request.user_profile = None
                request.is_staff = False
        else:
            request.user_profile = None
            request.is_staff = False
