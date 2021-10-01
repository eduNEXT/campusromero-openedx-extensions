"""
Context extender module for edx-platform account page
"""
from campusromero_openedx_extensions.custom_registration_form.models import CustomFormFields
from django.db import models


def get_fields(custom_form_model_instance):
    """Get the custom form fields from the model."""
    custom_fields = custom_form_model_instance._meta.fields
    blacklisted_fields = ["id", "user"]
    for field in custom_fields:
        if field.name in blacklisted_fields:
            continue
        if isinstance(field, (models.CharField, models.TextField)):
            yield field


def update_account_view(context, user):
    """Updates the context of the account settings page."""
    custom_form_model, _ = CustomFormFields.objects.get_or_create(user=user)
    extended_profile_fields = [
        {
            "field_name": field.name,
            "field_label": field.verbose_name,
            "field_type": "TextField" if not field.choices else "ListField",
            "field_options": [] if not field.choices else field.choices,
        }
        for field in get_fields(custom_form_model)
    ]
    context["extended_profile_fields"].extend(extended_profile_fields)


def update_account_serializer(data, user):
    """Updates the account serializer."""
    custom_form_model, _ = CustomFormFields.objects.get_or_create(user=user)
    extended_profile = data.get("extended_profile", {})
    custom_profile = [
        {
            "field_name": field.name,
            "field_value": getattr(custom_form_model, field.name, "")
        }
        for field in get_fields(custom_form_model)
    ]
    extended_profile.extend(custom_profile)
    data["extended_profile"].extend(extended_profile)


def partial_update_account(update, user):
    """Update the user data."""
    if 'extended_profile' in update:
        custom_form_model, _ = CustomFormFields.objects.get_or_create(user=user)
        new_extended_profile = update['extended_profile']

        for field in new_extended_profile:
            setattr(custom_form_model, field["field_name"], field['field_value'])

        custom_form_model.save()
