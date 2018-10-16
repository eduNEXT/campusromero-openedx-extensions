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
            'month_of_birth',
            'day_of_birth',
            'dni',
            'phone_number',
            'institution',
        )


    def __init__(self, *args, **kwargs):
        super(CustomForm, self).__init__(*args, **kwargs)
        self.fields['month_of_birth'].error_messages = {
            "required": _('Please enter your month of birth.'),
        }
        self.fields['day_of_birth'].error_messages = {
            "required": _('Please enter your day of birth.'),
        }
        self.fields['dni'].error_messages = {
            'required': _('Please enter DNI number.'),
            'invalid': _('This DNI number seems invalid, please check your input.'),
        }
        self.fields['phone_number'].error_messages = {
            'required': _('Please enter your phone number.'),
            'invalid': _('This Phone number seems invalid, please check your input.'),
        }
        self.fields['institution'].error_messages = {
            'required': _('Please enter your institution name.'),
            'invalid': _('This Institution name seems invalid, please check your input.'),
        }