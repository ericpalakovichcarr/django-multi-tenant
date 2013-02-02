from django.db import models
from tenant.models import TenantManager

class Thing(models.Model):
    name = models.CharField(max_length=100)
    tenant = models.ForeignKey("tenant.Tenant")
    objects = TenantManager()
    def __unicode__(self):
        return self.name