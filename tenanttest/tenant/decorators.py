import types

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

from tenant import get_tenant_model, get_tenant_from_request

def tenant_restricted(klass):
    """
    Decorator for model classes.  Restricts queryable records to ones that have their tenant set as the
    user's tenant in the request, or all records if the user doesn't have a set tenant.  Also removes the
    ability to change or set the tenant field in the admin for these users too.
    """
    tenant_model = get_tenant_model()
    if klass == tenant_model:
        return klass
    is_auth_user_model = settings.AUTH_USER_MODEL == "%s.%s" % (klass._meta.app_label, klass._meta.object_name)

    # Get all the Manager objects from the class
    potential_attrs = [attr for attr in dir(klass) if not attr.startswith("_")]
    managers = [getattr(klass, m) for m in potential_attrs if isinstance(getattr(klass, m), models.Manager)]

    # Update each Manager object so that it can only query data linked to the current user's tenant
    for manager in managers:
        _monkeypatch_get_query_set(manager)

    # Ensure the model's save method always sets the tenant to the current user's tenant
    #_monkeypatch_save(klass)

    # Make sure any tenant field's in the class can't be edited in the admin, and that it defaults to the
    # tenant assigned to the logged in user in the request.
    # The AUTH_USER_MODEL can have the tenant field managed by user's with a tenant of None, so the editable field
    # for the AUTH_USER_MODEL's tenant fields is handled in the admin form class.
    for tenant_field in tenant_model._get_tenant_fields_in(klass):
        klass._meta.get_field(tenant_field).default = get_tenant_from_request
        klass._meta.get_field(tenant_field).editable = is_auth_user_model

    return klass

def _monkeypatch_get_query_set(manager):
    # Save the old method so it can be referenced in the monkey patched method we're about to add
    manager.old_get_query_set_method = manager.get_query_set

    # Replace the old method with the new method
    manager.get_query_set = types.MethodType(
        _new_get_query_set_method,
        manager,
        manager.__class__
    )

def _new_get_query_set_method(self):
    """
    Replacement query set that forces the default manager of a model to restrict itself to the
    user's tenant from the request (no restriction if the user doesn't have a tenant).

    NOTE: Monkey patched in via the @tenant_restricted decorator.
    """
    qs = self.old_get_query_set_method()
    tenant = get_tenant_from_request()
    if tenant:
        tenant_model = get_tenant_model()
        for tenant_field in tenant_model._get_tenant_fields_in(self.model):
            qs = qs.filter(**{tenant_field: tenant})
    return qs
#
#def _monkeypatch_save(klass):
#    """Patch the model's save method so it runs tenant logic before saving the model."""
#    klass._pre_tenant_monkeypatch_save = klass.save
#    klass.save = _new_save_method
#
#def _new_save_method(self, *args, **kwargs):
#    """Force the model's tenant fields to be set to the user's tenant in the request."""
#    users_tenant = get_tenant_from_request()
#    for tenant_field in get_tenant_model()._get_tenant_fields_in(self):
#        current_tenant = getattr(self, tenant_field)
#        if current_tenant != users_tenant:
#            setattr(self, tenant_field, users_tenant)
#    self._pre_tenant_monkeypatch_save(*args, **kwargs)
