import os
import re
import base64
from datetime import datetime, timedelta
from django.conf import settings
from models import Hit, User

ID_NAME = "id"
SECONDS_TO_EXPIRE = 365 * 24 * 60 * 60
TIMEDELTA = timedelta(seconds=SECONDS_TO_EXPIRE)
IGNORE_PATHS = [
    re.compile("^/admin/*."),
    re.compile("^/__debug__/*."),
    re.compile("/favicon.ico"),
    re.compile("/static/favicon.ico"), ]


class FabvMiddleware(object):
    """
    Process a request using the response that will be sent.
    """
    def process_response(self, request, response):
        if not is_path_ignored(request.path):
            save_hit(request, response)

        try:
            if request.COOKIES.get('id', '') != request.fabv_user.key:
                set_cookie(response, request.fabv_user.key)
        except:
            pass  # Db error previously? TODO

        return response

    def process_request(self, request):
        request.fabv_user = get_fabv_user(request)


def get_fabv_user(request):
    # Identify the user. First by an id set in a cookie and then using
    # the clients ip address. If no id is present a new user is created.
    ip = get_client_ip(request)
    try:
        # If this value is set we have return user.
        id_value = request.COOKIES[ID_NAME]
        # Falls through if the key does not exist
        user = User.objects.get(key=id_value)
        if user.ip != ip:
            # Create a new user if this is a new IP
            user = User(key=user.key, ip=ip)
            user.save()
    except:
        # Try to find the client IP in the database.
        users = User.objects.filter(ip=ip)
        # The site has been browsed before from this address.
        if users.exists():
            user = users[0]  # More users with this IP, can happen if
                             # users from different IP start to use the
                             # same IP.
        else:
            # The site has not been used by this ip and no cookie is
            # set, so create a user.
            user = User(key=create_id(), ip=ip)
            user.save()
    return user


def is_path_ignored(path):
    """
    Checks whether the current path is in IGNORE_PATHS.
    """
    for test_path in IGNORE_PATHS:
        match = test_path.match(path)
        if match is not None:
            return True
    return False


def save_hit(request, response):
    """
    Save a hit on a page.
    """
    try:
        username = request.user.username
    except:
        username = ""
    try:
        h = Hit(user=request.fabv_user, username=username,
                path=request.path[:200],
                status_code=response.status_code,
                referer=request.META.get('HTTP_REFERER', ''),
                user_agent=request.META.get('HTTP_USER_AGENT', ''))
        h.save()
    except:
        pass  # What is a sensible action? TODO


def create_id():
    return base64.b64encode(os.urandom(16))

def set_cookie(response, id_value):
    expires = datetime.strftime(datetime.utcnow() + TIMEDELTA,
                                "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(ID_NAME, id_value,
                        max_age=SECONDS_TO_EXPIRE,
                        expires=expires,
                        domain=settings.SESSION_COOKIE_DOMAIN,
                        secure=settings.SESSION_COOKIE_SECURE or None)
    return id_value


# From http://stackoverflow.com/a/5976065/862288
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
