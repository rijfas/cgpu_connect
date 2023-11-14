from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME


def login_required_with_type(type):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.type == type,
        login_url=None,
        redirect_field_name=REDIRECT_FIELD_NAME,
    )
    return actual_decorator
