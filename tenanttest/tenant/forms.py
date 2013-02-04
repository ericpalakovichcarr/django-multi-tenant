from django import forms
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm

# Pulled from UserCreationForm to replace auth.User with the AUTH_USER_MODEL from settings where nessecary.
# Otherwise exact copy from parent class
# There's a ticket to make this nonsense unessecary, but it looks like it won't make it into 1.5
class OrgUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()

    def clean_username(self):
        user_model = get_user_model()
        username = self.cleaned_data["username"]
        try:
            user_model.objects.get(username=username)
        except get_user_model().DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])
