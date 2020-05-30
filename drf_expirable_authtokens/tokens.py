import warnings

from django.contrib.auth import get_user_model

from django_tokens import HMACToken

from .settings import setting, settings, default_settings


class ExpirableToken(HMACToken):
    """
    Stateless expirable authorization token.

    Attributes:
        salt (str): Salt used in the signature. Defaults to
            settings.EXPIRABLE_TOKEN_SALT. Leaving this as the default or using
            the same salt for different projects is a security risk.

        max_age (int): The lifetime of the token in seconds before its key
            becomes invalid. Defaults to settings.EXPIRABLE_TOKEN_MAX_AGE.
    """

    _user = None

    def __init__(self, user):
        super().__init__(nat_key=user.get_username(), last_login=user.last_login)
        self._user = user

    @property
    def user(self):
        if self._user is None:
            User = get_user_model()
            self._user = User.objects.get_by_natural_key(self.nat_key)
        return self._user

    def check_validity(self):
        if self.last_login != self.user.last_login:
            raise self.AlreadyUsed

    @classmethod
    def get_max_age(cls):
        return setting(cls.max_age, settings.EXPIRABLE_TOKEN_MAX_AGE)

    @classmethod
    def get_salt(cls):
        salt = setting(cls.salt, settings.EXPIRABLE_TOKEN_SALT)
        if salt == default_settings.EXPIRABLE_TOKEN_SALT:
            warnings.warn(
                'Leaving the ExpirableToken salt as the '
                'default value is a security risk.'
            )
        return salt
