from django.apps import apps
from django.contrib import admin
from graphql_jwt.refresh_token.models import RefreshToken
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from businessLogic.models import ServiceCategory
from smileDesign.models import SmileCategory, SmileColor
from import_export.admin import ImportExportModelAdmin
from import_export import resources

from django.db.models import ManyToManyField



def create_model_object_meta(model):
    return type('Meta', (object, ) ,dict(model=model,))



exempted_field_types = (ManyToManyField, )
def getFieldsModel(model):
    return [field.name for field in model._meta.get_fields() if not isinstance(field, exempted_field_types)]



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


custome_admin_models = [ServiceCategory, SmileCategory, SmileColor, RefreshToken]



for model in models:
    if model == ServiceCategory or model == SmileCategory or model == SmileColor or model == RefreshToken:
        continue
    try:
        meta_class = create_model_object_meta(model)
        modelResource = type(f'{model.__name__}Resource', (resources.ModelResource,), dict(Meta=meta_class,))
        adminModel = type(f'{model.__name__}Admin', (ImportExportModelAdmin,), dict(resource_class=model))
        admin.site.register(model, adminModel)
    except admin.sites.AlreadyRegistered:
        pass

