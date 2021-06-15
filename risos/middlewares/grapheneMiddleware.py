from graphql_jwt.utils import get_payload
from django.contrib.auth.models import User
from django.http import HttpResponse


class CustomAuth(object):

    done = False

    def resolve(self, next, root, info, **args):
        if info.field_name == "tokenAuth":
            self.done = True
        if self.done:
            return next(root, info, **args)
        else:
            http_token = info.context.META.get("HTTP_TOKEN")
            response = HttpResponse()
            try:
                try:
                    token = http_token.split(" ")[-1]
                except AttributeError as e:
                    response.status_code = 403
                    return response
                try:
                    phone_number = get_payload(token)["username"]
                except:
                    response.status_code = 403
                    return response
                user = User.objects.get(username = phone_number)
                if (user.is_authenticated and self.validDoctor(user)):
                    self.done = True
                    return next(root, info, **args)
                else:
                    response.status_code = 403
            
            except AttributeError:
                return next(root, info, **args)
            return response

    def validDoctor(self, user):
        doctor = user.profile
        if doctor.role == "doctor":
            return True
        return False