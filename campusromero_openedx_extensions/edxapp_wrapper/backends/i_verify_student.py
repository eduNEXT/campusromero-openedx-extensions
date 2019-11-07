"""
Backend abstraction
"""

from lms.djangoapps.verify_student.models import SoftwareSecurePhotoVerification  # pylint: disable=import-error


def get_software_photo_verification():
    """
    Get SoftwareSecurePhotoVerification model from edxapp
    """
    return SoftwareSecurePhotoVerification
