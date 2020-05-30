from distutils.core import setup

setup(
    name='DRF expirable auth tokens',
    version='0.0.1',
    description='Drop in replacement for DRF .',
    long_description=open('README.rst').read(),
    install_requires=['django_tokens @ git+https://github.com/AlbinLindskog/django_tokens'],
    packages=['drf_expirable_authtokens'],
    author='Albin Lindskog',
    author_email='albin@zerebra.com',
    url='https://github.com/albinlindskog/drf_expirable_authtokens',
    zip_safe=True,
)
