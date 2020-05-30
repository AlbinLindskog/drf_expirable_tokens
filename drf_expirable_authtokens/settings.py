from django.conf import settings


class DEFAULTS:
    EXPIRABLE_TOKEN_SALT = 'drf_expirable_authtokens.salt'
    EXPIRABLE_TOKEN_MAX_AGE = 60 * 60 * 24
    EXPIRABLE_TOKEN_RAISE_INVALID = True


class TokenSettings:
    """
    Custom settings module for django_tokens. Checks if the requested setting
    is present in the user provided django settings module, if not it fall
    backs to the projects default settings.
    """

    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        self._user_settings = user_settings
        self._defaults = defaults

    def __getattr__(self, attr):
        fallback = getattr(self._defaults, attr)
        return getattr(self._user_settings, attr, fallback)


settings = TokenSettings(settings, DEFAULTS())


default_settings = DEFAULTS()


def setting(val, default):
    return val if val is not None else default
