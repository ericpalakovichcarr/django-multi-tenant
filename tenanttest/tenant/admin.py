from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from tenant.forms import OrgUserCreationForm
from tenant import get_tenant_from_request, get_tenant_model

def auth_model_tenant_fields():
    return get_tenant_model()._get_tenant_fields_in(get_user_model())

class OrgUserAdmin(UserAdmin):
    add_form = OrgUserCreationForm

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': tuple(auth_model_tenant_fields()) + ('username', 'password1', 'password2')}
        ),
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(OrgUserAdmin, self).get_fieldsets(request, obj)
        if get_tenant_from_request() is not None:
            fields = list(fieldsets[0][1]['fields'])
            tenant_fields = auth_model_tenant_fields()
            for field_to_remove in [f for f in tenant_fields if f in fields]:
                fields.remove(field_to_remove)
            fieldsets[0][1]['fields'] = tuple(fields)
        return fieldsets
