
""" Backend abstraction. """
from importlib import import_module
from django.conf import settings


def get_software_photo_verification(*args, **kwargs):
    """ Return render to response. """

    backend_function = settings.CAMPUS_VERIFYSTUDENT_MODULE
    backend = import_module(backend_function)

    return backend.get_software_photo_verification(*args, **kwargs)
