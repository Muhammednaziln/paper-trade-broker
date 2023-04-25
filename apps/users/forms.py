from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as CoreUserCreationForm, UsernameField

User = get_user_model()


class UserCreationForm(CoreUserCreationForm):

    class Meta:
        model = User
        fields = ("username", 'date_of_birth', 'email', 'first_name', 'last_name')
        field_classes = {'username': UsernameField}
