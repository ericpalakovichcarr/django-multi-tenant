from django.contrib import admin
from django.contrib.auth.models import Group

from org.models import Organization, User
from tenant.admin import OrgUserAdmin

admin.site.register(Organization)
admin.site.register(User, OrgUserAdmin)
admin.site.unregister(Group) # <<--- New group model is created for our custom user model by Django, so get rid of old one
