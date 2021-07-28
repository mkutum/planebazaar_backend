from functools import wraps
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from rest_framework import status


def login_required(func):
    @wraps(func)
    def wrapped_func(obj, request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
            return HttpResponse('Login Required.', status=status.HTTP_403_FORBIDDEN)
        elif not request.user.is_active:
            return HttpResponse('User not active.', status=status.HTTP_403_FORBIDDEN)
        else:
            return func(obj, request, *args, **kwargs)

    return wrapped_func
