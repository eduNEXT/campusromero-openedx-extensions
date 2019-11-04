# -*- coding: utf-8 -*-
"""
Admin file.
"""
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import CustomFormFields


@admin.register(CustomFormFields)
class CustomFormFieldsAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)


class CustomFormFieldsInline(admin.StackedInline):
    """ Inline admin interface for CustomFormFields model. """
    model = CustomFormFields
    can_delete = False
    verbose_name_plural = _('Custom Fields')
