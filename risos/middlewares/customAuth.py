from graphql_jwt.utils import get_payload
from django.contrib.auth.models import User
from django.http import HttpResponse

class CustomAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # for key, val in request.META.items():
        #     print(key, ":", val, "===>", type(val))
        
        input = request.META.get("wsgi.input")
        print((request.method))
        print(request.session.keys())
        # print((request.body))
        http_token = request.META.get("HTTP_TOKEN")
        response = HttpResponse()
        try:
            token = http_token.split(" ")[-1]
            phone_number = get_payload(token)["username"]
            user = User.objects.get(username = phone_number)
            if (user.is_authenticated and self.validDoctor(user)):
                response = self.get_response(request)
            else:
                response.status_code = 403
        
        except:
            response.status_code = 403

        return response


    def validDoctor(self, user):
        doctor = user.profile
        if doctor.role == "doctor":
            return True
        return True