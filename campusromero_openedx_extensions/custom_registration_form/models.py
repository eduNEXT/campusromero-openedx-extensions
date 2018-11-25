# -*- coding: utf-8 -*-
"""
File to define CustomFormFields model.
"""
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .choices import MONTH_OF_BIRTH, DAY_OF_BIRTH

# Backwards compatible settings.AUTH_USER_MODEL
USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class CustomFormFields(models.Model):
    """
    Holds extra info to be, used during
    user registration as a form extension.
    """
    user = models.OneToOneField(USER_MODEL, null=True)
    month_of_birth = models.CharField(
        verbose_name=_("Month Of Birth"),
        blank=True,
        null=True,
        max_length=2,
        choices=MONTH_OF_BIRTH
    )
    day_of_birth = models.CharField(
        verbose_name=_("Day Of Birth"),
        blank=True,
        null=True,
        max_length=2,
        choices=DAY_OF_BIRTH
    )
    dni = models.TextField(
        verbose_name=_("DNI"),
        max_length=10
    )
    phone_number = models.CharField(
        verbose_name=_("Phone Number"),
        max_length=60
    )
    institution = models.TextField(
        verbose_name=_("Institution"),
        blank=True,
        null=True,
        max_length=60
    )
