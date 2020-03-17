from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.throttling import AnonRateThrottle

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user

from .serializers import UserSerializer


def _send400(msg):
    data = {'message': msg}
    return Response(data, status=400)


class AuthViewSet(viewsets.GenericViewSet):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer

    def get_object(self):
        parsed = UserSerializer(data=self.request.data)
        return parsed.data if parsed.is_valid() else None

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request, *args, **kwargs):
        data = {}
        auth_obj = self.get_object()

        if not auth_obj:
            return _send400('invalid username or password')

        potential_user = User.objects.filter(
            username=auth_obj['username']).first()
        if not potential_user:
            return _send400('non existent user')

        if not potential_user.is_active:
            return _send400('User is not allowed to login')

        auth_user = authenticate(
            request, username=auth_obj['username'], password=auth_obj['password'])

        if not auth_user:
            return _send400('incorrect password')

        if auth_user == potential_user:
            login(request, auth_user)
            req_flds = ('id', 'username', 'is_active', 'is_anonymous', 'is_authenticated',
                        'is_staff', 'is_superuser', 'last_login', 'first_name', 'last_name')
            headers = {}
            data = {}
            for fld in req_flds:
                data[fld] = getattr(potential_user, fld)
            headers['Cache-Control'] = 'private, no-cache'
            response = Response(data, headers=headers, status=200)
            response.set_cookie('authenticated', value='True', secure=True)
            return response

        return Response(data, status=400)

    @action(detail=False, methods=['get'], url_path='logout')
    def logout(self, request, *args, **kwargs):
        headers = {}
        current_user = get_user(request)
        response = Response({}, headers=headers, status=401)
        if current_user.is_authenticated:
            headers['Cache-Control'] = 'private, no-cache'
            logout(request)
            data = {'logged_out': True}
            response = Response(data, headers=headers, status=401)
            response.delete_cookie('authenticated')
        return response

    @action(detail=False, methods=['get'], url_path='users')
    def logout(self, request, *args, **kwargs):
        headers = {}
        user_list = User.objects.filter(is_active=True)        
        response = Response({}, headers=headers, status=404)
        if len(user_list) > 0:
            user_names = [user.username for user in user_list]
            response = Response({'users':user_names}, headers=headers, status=200)
        return response
