from django.apps import apps
from django.contrib import admin
from graphql_jwt.refresh_token.models import RefreshToken
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
# Register your models here.
from businessLogic.models import ServiceCategory
from smileDesign.models import SmileCategory, SmileColor
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Teeth



class TeethAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_tooths', 'related_smile_color', 'related_smile_category']

    def get_tooths(self, obj):
        return obj.Tooths.all()


admin.site.register(Teeth, TeethAdmin)



def create_model_object_meta(model):
    return type('Meta', (object, ) ,dict(model=model,))




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
        meta_class = create_model_object_meta(model)
        modelResource = type(f'{model.__name__}Resource', (resources.ModelResource,), dict(Meta=meta_class,))
        adminModel = type(f'{model.__name__}Admin', (ImportExportModelAdmin,), dict(resource_class=model,))
        admin.site.register(model, adminModel)
    except admin.sites.AlreadyRegistered:
        pass
