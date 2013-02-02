from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

from request_provider.signals import get_request

class Tenant(models.Model):
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name

class TenantManager(models.Manager):
    def get_query_set(self):
        qs = super(TenantManager, self).get_query_set()
        request = get_request()
        if request:
            tenant_qs = Tenant.objects.filter(tenantuser__id=request.session.get('_auth_user_id'))
            if tenant_qs.count() == 1:
                tenant_fields = [field.name for field in self.model._meta.fields if field.rel and field.rel.to == Tenant]
                for tenant_field in tenant_fields:
                    qs = qs.filter(**{tenant_field: tenant_qs.get()})
        return qs

class TenantUserManager(UserManager):
    def get_query_set(self):
        qs = super(TenantUserManager, self).get_query_set()
        request = get_request()
        if request:
            tenant_qs = Tenant.objects.filter(tenantuser__id=request.session.get('_auth_user_id'))
            if tenant_qs.count() == 1:
                tenant_fields = [field.name for field in self.model._meta.fields if field.rel and field.rel.to == Tenant]
                for tenant_field in tenant_fields:
                    qs = qs.filter(**{tenant_field: tenant_qs.get()})
        return qs

class TenantUser(AbstractUser):
    tenant = models.ForeignKey('tenant.Tenant', null=True, blank=True)
    objects = TenantUserManager()
