"""
Resources module for the user import export feature.
"""
import logging
from import_export import resources, fields, widgets
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text

from campusromero_openedx_extensions.custom_registration_form.models import CustomFormFields
from student.models import UserProfile  # pylint: disable=import-error


class CustomCharWidget(widgets.CharWidget):
    """
    Custom Char Widget used in the UserResource class.
    """

    def clean(self, value, row=None, *args, **kwargs):
        """
        Forcing the value to be text without the decimal part
        """
        if isinstance(value, float):
            value = force_text(int(value))
        return value


class UserResource(resources.ModelResource):
    """
    Using a custom widget on char fields composed by numbers to
    prevent issue when importing with XLS

    More details here:
    https://github.com/django-import-export/django-import-export/issues/96
    """
    password = fields.Field(attribute='password', widget=CustomCharWidget())

    # UserProfile columns
    name = fields.Field(attribute='name')
    gender = fields.Field(attribute='gender')
    city = fields.Field(attribute='city')
    year_of_birth = fields.Field(attribute='year_of_birth', widget=CustomCharWidget())

    # CustomFormFields columns
    day_of_birth = fields.Field(attribute='day_of_birth', widget=CustomCharWidget())
    month_of_birth = fields.Field(attribute='month_of_birth', widget=CustomCharWidget())
    dni = fields.Field(attribute="dni", widget=CustomCharWidget())
    phone_number = fields.Field(attribute="phone_number", widget=CustomCharWidget())
    institution = fields.Field(attribute="institution")

    class Meta:
        """
        Resource meta class.
        """
        model = User
        import_id_fields = ['id']
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'dni',
            'phone_number',
            'id',
            'name',
            'gender',
            'city',
            'year_of_birth',
            'institution',
            'password',
            'date_joined',
            'day_of_birth',
            'month_of_birth',
        )
        export_order = (
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            'email',
            'dni',
            'phone_number',
            'name',
            'gender',
            'city',
            'day_of_birth',
            'month_of_birth',
            'year_of_birth',
            'institution',
            'date_joined',
        )

    def dehydrate_dni(self, obj):
        """
        Dehydrate dni field.
        """
        dni = ''
        try:
            dni = obj.dni
        except AttributeError:
            pass

        if not dni:
            try:
                dni = CustomFormFields.objects.get(user=obj).dni  # pylint: disable=no-member
            except CustomFormFields.DoesNotExist:  # pylint: disable=no-member
                pass

        return dni

    def dehydrate_phone_number(self, obj):
        """
        Dehydrate phone number field.
        """
        phone_number = ''
        try:
            phone_number = obj.phone_number
        except AttributeError:
            pass

        if not phone_number:
            try:
                phone_number = CustomFormFields.objects.get(user=obj).phone_number  # pylint: disable=no-member
            except CustomFormFields.DoesNotExist:  # pylint: disable=no-member
                pass

        return phone_number

    def dehydrate_name(self, obj):
        """
        Dehydrate name field.
        """
        name = ''
        try:
            name = obj.name
        except AttributeError:
            pass

        if not name:
            try:
                name = UserProfile.objects.get(user=obj).name
            except UserProfile.DoesNotExist:
                pass

        return name

    def dehydrate_gender(self, obj):
        """
        Dehydrate gender field.
        """
        gender = None
        try:
            gender = obj.gender
        except AttributeError:
            pass

        if not gender:
            try:
                gender = UserProfile.objects.get(user=obj).gender
            except UserProfile.DoesNotExist:
                pass

        return gender

    def dehydrate_city(self, obj):
        """
        Dehydrate city field.
        """
        city = None
        try:
            city = obj.city
        except AttributeError:
            pass

        if not city:
            try:
                city = UserProfile.objects.get(user=obj).city
            except UserProfile.DoesNotExist:
                pass

        return city

    def dehydrate_day_of_birth(self, obj):
        """
        Dehydrate day of birth field.
        """
        day_of_birth = None
        try:
            day_of_birth = obj.day_of_birth
        except AttributeError:
            pass

        if not day_of_birth:
            try:
                day_of_birth = CustomFormFields.objects.get(user=obj).day_of_birth  # pylint: disable=no-member
            except CustomFormFields.DoesNotExist:  # pylint: disable=no-member
                pass

        return day_of_birth

    def dehydrate_month_of_birth(self, obj):
        """
        Dehydrate month of birth.
        """
        month_of_birth = None
        try:
            month_of_birth = obj.month_of_birth
        except AttributeError:
            pass

        if not month_of_birth:
            try:
                month_of_birth = CustomFormFields.objects.get(user=obj).month_of_birth  # pylint: disable=no-member
            except CustomFormFields.DoesNotExist:  # pylint: disable=no-member
                pass

        return month_of_birth

    def dehydrate_year_of_birth(self, obj):
        """
        Dehydrate year of birth.
        """
        year_of_birth = None
        try:
            year_of_birth = obj.year_of_birth
        except AttributeError:
            pass

        if not year_of_birth:
            try:
                year_of_birth = UserProfile.objects.get(user=obj).year_of_birth
            except UserProfile.DoesNotExist:
                pass

        return year_of_birth

    def dehydrate_institution(self, obj):
        """
        Dehydrate insitution field.
        """
        institution = ''
        try:
            institution = obj.institution
        except AttributeError:
            pass

        if not institution:
            try:
                institution = CustomFormFields.objects.get(user=obj).institution  # pylint: disable=no-member
            except CustomFormFields.DoesNotExist:  # pylint: disable=no-member
                pass

        return institution

    def before_save_instance(self, instance, using_transactions, dry_run):
        """
        Actions to do before save instance
        """
        duplicate_email = False
        error_duplicate_email = 'Advertencia_Sbs1: \"Duplicate entry \'' + str(instance.email) + '\' for key \'email\''  # pylint: disable=line-too-long

        # Name, first_name and last_name fields must not be None (allowed to be blank)
        instance.name = instance.name or ''
        instance.first_name = instance.first_name or ''
        instance.last_name = instance.last_name or ''

        if not instance.id:
            duplicate_email = User.objects.filter(email=instance.email).exists()
        elif instance.email and not instance.email == User.objects.get(id=instance.id).email:
            duplicate_email = User.objects.filter(email=instance.email).exists()

        if duplicate_email:
            raise Exception(error_duplicate_email)

        new_pass = ''

        if not instance.password:
            new_pass = '1234'
        elif isinstance(instance.password, int) and str(instance.password)[-2:] == '.0':
            new_pass = str(instance.password)[:-2]
        else:
            new_pass = str(instance.password)

        instance.password = make_password(new_pass, salt=None, hasher='default')

    def after_save_instance(self, instance, using_transactions, dry_run):
        """
        Actions to do after save instance.
        """
        if not dry_run:
            if isinstance(instance.dni, int) and str(instance.dni)[-2:] == '.0':
                instance.dni = str(instance.dni)[:-2]

            if isinstance(instance.phone_number, int) and str(instance.phone_number)[-2:] == '.0':
                instance.phone_number = str(instance.phone_number)[:-2]

            if not isinstance(instance.year_of_birth, int):
                instance.year_of_birth = int(instance.year_of_birth)

            try:
                userprofile, created_userprofile = UserProfile.objects.get_or_create(
                    user=instance,
                    defaults={
                        'name': instance.name,
                        'gender': instance.gender,
                        'city': instance.city,
                        'year_of_birth': instance.year_of_birth,
                    }
                )

                if not created_userprofile:
                    userprofile.name = instance.name
                    userprofile.gender = instance.gender
                    userprofile.city = instance.city
                    userprofile.year_of_birth = instance.year_of_birth
                    userprofile.save()

                custom_fields, created_customfields = CustomFormFields.objects.get_or_create(  # pylint: disable=no-member
                    user=instance,
                    defaults={
                        'dni': instance.dni,
                        'phone_number': instance.phone_number,
                        'institution': instance.institution,
                        'day_of_birth': instance.day_of_birth,
                        'month_of_birth': instance.month_of_birth,
                    }
                )

                if not created_customfields:
                    custom_fields.dni = instance.dni
                    custom_fields.phone_number = instance.phone_number
                    custom_fields.institution = instance.institution
                    custom_fields.day_of_birth = instance.day_of_birth
                    custom_fields.month_of_birth = instance.month_of_birth
                    custom_fields.save()

            except Exception as e:
                logging.info(e)
