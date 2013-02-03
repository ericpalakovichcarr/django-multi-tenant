from django.db import models
from django.contrib.auth.models import AbstractUser
from tenant.decorators import tenant_restricted

@tenant_restricted
class Organization(models.Model):
    name = models.CharField(max_length=100)
    _tenant_manager = models.Manager()
    def __unicode__(self):
        return self.name

@tenant_restricted
class User(AbstractUser):
    organization = models.ForeignKey(Organization, null=True, blank=True, editable=False)
