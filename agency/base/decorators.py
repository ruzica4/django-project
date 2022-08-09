from django.core.exceptions import PermissionDenied
from .models import BaseUser


def user_is_agency(function):
    def wrap(request, *args, **kwargs):
        user = BaseUser.objects.get(username=request.user)
        if user.user_type == 'AGENCY':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def user_is_tourist(function):
    def wrap(request, *args, **kwargs):
        user = BaseUser.objects.get(username=request.user)
        if user.user_type == 'TOURIST':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def user_is_logged_out(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user == 'AnonymousUser':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
