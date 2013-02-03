from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured

class TenantModel(models.Model):
    _tenant_manager = models.Manager()

    @classmethod
    def _get_tenant_fields_in(klass, model):
        """
        Gets the fields in a Model that are a ForeignKey to the model defined by the setting TENANT_MODEL.
        """
        return [field.name for field in model._meta.fields if field.rel and field.rel.to == klass]

    @classmethod
    def _get_auth_user_field_name(klass):
        """
        Gets the field in the TENANT_MODEL that is a ForeignKey to the AUTH_USER_MODEL.
        """
        fields = [rm for rm in klass._meta.get_all_related_objects() if rm.model == get_user_model()]
        if len(fields) == 0:
            raise ImproperlyConfigured("Model %s requires a ForeignKey field to %s" % (settings.AUTH_USER_MODEL, settings.TENANT_MODEL))
        elif len(fields) > 1:
            raise ImproperlyConfigured("Model %s requires one and only one ForeignKey field to %s.  Found %s!" %
                                       (settings.AUTH_USER_MODEL, settings.TENANT_MODEL, len(fields)))
        return fields[0].var_name
