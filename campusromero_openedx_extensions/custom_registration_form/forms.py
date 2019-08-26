"""
Model forms file.
"""
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from .models import CustomFormFields


class CustomForm(ModelForm):
    """
    Class to defined the form used from CustomFormFields model.
    """
    class Meta(object):
        """
        Class to initialize the form.
        """
        model = CustomFormFields
        fields = (
            'day_of_birth',
            'month_of_birth',
            'dni',
            'phone_number',
            'institution',
        )

    def __init__(self, *args, **kwargs):
        super(CustomForm, self).__init__(*args, **kwargs)
        self.fields['month_of_birth'].error_messages = {
            "invalid": _('This month is not valid, please check your input.'),
        }
        self.fields['day_of_birth'].error_messages = {
            "invalid": _('This day number is not valid, please check your input.'),
        }
        self.fields['dni'].error_messages = {
            'invalid': _('This DNI number seems invalid, please check your input.'),
        }
        self.fields['phone_number'].error_messages = {
            'invalid': _('This Phone number seems invalid, please check your input.'),
        }
        self.fields['institution'].error_messages = {
            'invalid': _('This Institution name seems invalid, please check your input.'),
        }
