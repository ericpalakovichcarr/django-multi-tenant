from django.db import models
from tenant.decorators import tenant_restricted

@tenant_restricted
class Thing(models.Model):
    org = models.ForeignKey("org.Organization", editable=False)
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name
