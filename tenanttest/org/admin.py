from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import (UserCreationForm)
from django.contrib.auth.models import Group

from org.models import Organization, User

# Pulled from UserCreationForm to replace auth.User with org.User where nessecary.
# Otherwise exact copy from parent class
# There's a ticket to make this nonsense unessecary, but it looks like it won't make it into 1.5
class OrgUserCreationForm(UserCreationForm):
    class Meta:
        model = User

    def __init__(self):
        pass

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

class OrgUserAdmin(UserAdmin):
    add_form = OrgUserCreationForm
    def get_fieldsets(self, request, obj=None):
        fieldsets = super(OrgUserAdmin, self).get_fieldsets(request, obj)
        fieldsets[None]['fields'] = ('organization', 'username', 'password1', 'password2')

admin.site.register(Organization)
admin.site.register(User, OrgUserAdmin)
admin.site.unregister(Group) # <<--- New group model is created for our custom user model by Django, so get rid of old one
