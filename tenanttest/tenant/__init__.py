from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from request_provider.signals import get_request

def get_tenant_model():
        """
        Gets the Django model defined by the user via the TENANT_MODEL setting.
        """
        from django.conf import settings
        from django.db.models import get_model

        try:
            app_label, model_name = settings.TENANT_MODEL.split('.')
        except ValueError:
            raise ImproperlyConfigured("TENANT_MODEL must be of the form 'app_label.model_name'")
        tenant_model = get_model(app_label, model_name, only_installed=False)
        if tenant_model is None:
            raise ImproperlyConfigured("TENANT_MODEL refers to model '%s' that has not been installed" % settings.TENANT_MODEL)
        return tenant_model

def get_tenant_from_request(request=None):
    """
    Gets the tenant for the user in the request.  If we're not in a web request, or the user doesn't
    have a tenant defined, returns None.
    """
    request = request or get_request()
    if request:
        tenant_model = get_tenant_model()
        user_id_field = '%s__id' % tenant_model._get_auth_user_field_name()

        # Query for a tenant who has the user defined in the request's session
        tenant_qs = tenant_model._tenant_manager.filter(**{user_id_field:request.session.get('_auth_user_id')})
        num_tenants = tenant_qs.count()
        if num_tenants == 1:
            return tenant_qs.get()