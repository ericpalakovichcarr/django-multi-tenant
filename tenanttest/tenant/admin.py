from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import (UserCreationForm, UserChangeForm)
from django.contrib.auth.models import Group
from django.utils.translation import ugettext, ugettext_lazy as _

from tenant.models import Tenant, TenantUser

class TenantUserCreationForm(UserCreationForm):
    class Meta:
        model = TenantUser

    def clean_username(self):
        # Pulled from UserCreationForm to replace User with TenantUser where nessecary.
        # Otherwise exact copy from parent class
        username = self.cleaned_data["username"]
        try:
            TenantUser.objects.get(username=username)
        except TenantUser.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def save(self, commit=True):
        user = super(TenantUserCreationForm, self).save(commit=False)
        user.tenant = self.cleaned_data["tenant"]
        if commit:
            user.save()
        return user

class TenantUserAdmin(UserAdmin):
    add_form = TenantUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('tenant', 'username', 'password1', 'password2')}
        ),
    )

admin.site.register(Tenant)
admin.site.register(TenantUser, TenantUserAdmin)
admin.site.unregister(Group)
