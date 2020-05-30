from django.utils.translation import ugettext_lazy as _

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .tokens import ExpirableToken
from .settings import setting, settings


class ExpirableTokenAuthentication(TokenAuthentication):
    """
    An extension of Django REST frameworks TokenAuthentication that uses
    stateless, expirable HMAC-based tokens instead.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the keyword string, e.g:

        "Authorization: Token eyJuYXRfa2V5IjoiZGhhcm9jIiwibGFzdF9sb2dpbiI6bnVsbH0:1jexQY:k9lgfAGU0mb1pr1FKWCGtGeLmyU"

    Attributes:
        keyword (str): Keyword used in the header. The default is 'Token.

        model (obj): Token model to used. Defaults to ExpirableToken.

        raise_invalid (bool): Whether to raise AuthenticationFailed if a user
            provides an invalid token. Defaults to
            settings.EXPIRABLE_TOKEN_RAISE_INVALID.

            Setting this to False  allows you to use both
            ExpirableTokenAuthentication and TokenAuthentication with the same
            keyword in the same project. If this is True will
            ExpirableTokenAuthentication raise  AuthenticationFailed and
            short circuit the authentication when it encounters a regular
            authentication token, since those are not valid ExpirableTokens.
    """

    keyword = 'Token'
    model = ExpirableToken
    raise_invalid = None

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.from_key(key)
        except model.DoesNotExist:
            if self.get_raise_invalid():
                raise AuthenticationFailed(_('Invalid token.'))
            else:
                return None

        if not token.user.is_active:
            raise AuthenticationFailed(_('User inactive or deleted.'))

        return token.user, token

    @classmethod
    def get_raise_invalid(cls):
        return setting(
            cls.raise_invalid, settings.EXPIRABLE_TOKEN_RAISE_INVALID
        )
