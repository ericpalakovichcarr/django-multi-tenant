from django.db import models
from django.contrib.auth.models import AbstractUser
from tenant.models import TenantModel
from tenant.decorators import tenant_restricted

class Organization(TenantModel):
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name

@tenant_restricted
class User(AbstractUser):
    organization = models.ForeignKey(Organization, null=True, blank=True)
