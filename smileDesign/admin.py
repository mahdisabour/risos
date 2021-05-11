from django.apps import apps
from django.contrib import admin
from graphql_jwt.refresh_token.models import RefreshToken
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
# Register your models here.
from businessLogic.models import ServiceCategory
from smileDesign.models import SmileCategory, SmileColor


class MyServiceCategory(TreeAdmin):
    form = movenodeform_factory(ServiceCategory)


admin.site.register(ServiceCategory, MyServiceCategory)


class MySmileColor(TreeAdmin):
    form = movenodeform_factory(SmileColor)


admin.site.register(SmileColor, MySmileColor)


class MySmileCategory(TreeAdmin):
    form = movenodeform_factory(SmileCategory)


admin.site.register(SmileCategory, MySmileCategory)
models = apps.get_models()

for model in models:
    if model == ServiceCategory or model == SmileCategory or model == SmileColor or model == RefreshToken:
        continue
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
