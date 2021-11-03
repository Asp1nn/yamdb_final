from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
import six


from rest_framework.response import Response


User = get_user_model()


def send_confirmation_code(email, confirmation_code):
    data = f'Your confirmation code: {confirmation_code}'
    send_mail(
        'Welcome!', data, "YaMDB", [email], fail_silently=True
    )
    return Response('Confirmation code has been sent to your email')


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk)
            + six.text_type(timestamp)
            + six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


def set_username(email):
    username = email.split('@')[0]
    counter = 1
    while User.objects.filter(username=username):
        username = username + str(counter)
        counter += 1
    return username
