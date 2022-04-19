import datetime
import jwt
from rest_framework.authentication import BaseAuthentication
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
from app import settings

# https://dev.to/a_atalla/django-rest-framework-custom-jwt-authentication-5n5
class Jwt(object):
    def generate_access_token(id, data):
        expires_at = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        access_token_payload = {
            'id': id,
            'data': data,
            'exp': expires_at,
            'iat': datetime.datetime.utcnow(),
        }
        access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm='HS256')
        return access_token, expires_at

    def generate_refresh_token(id, data):
        refresh_token_payload = {
            'id': id,
            'data': data,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow()
        }
        refresh_token = jwt.encode(refresh_token_payload, settings.SECRET_KEY, algorithm='HS256')
        return refresh_token
    
    def authenticate(request):
        access_token = request.COOKIES.get('access_token') 
        if access_token is None:
            authorization_heaader = request.headers.get('Authorization')
            if not authorization_heaader:
                return None
            access_token = authorization_heaader.split(' ')[1]
        try:
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            # raise exceptions.AuthenticationFailed('access_token expired')
            return None
        except IndexError:
            # raise exceptions.AuthenticationFailed('Token prefix missing')
            return None
        return payload

class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        # Return the failure reason instead of an HttpResponse
        return reason

class SafeJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        authorization_heaader = request.headers.get('Authorization')
        if not authorization_heaader:
            return None
        try:
            # header = 'Token xxxxxxxxxxxxxxxxxxxxxxxx'
            access_token = authorization_heaader.split(' ')[1]
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')
        self.enforce_csrf(request)
        return payload

    def enforce_csrf(self, request):
        check = CSRFCheck()
        # populates request.META['CSRF_COOKIE'], which is used in process_view()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        print(reason)
        if reason:
            raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)