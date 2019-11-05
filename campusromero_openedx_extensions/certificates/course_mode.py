"""
Change the course enrollment mode.
"""
import logging

from .edxapp_dependencies import (
    CourseMode,
    CourseEnrollment,
    CertificateWhitelist,
)

LOG = logging.getLogger(__name__)


def change_course_mode(course, student):
    """
    Change the course enrollment mode to 'verified',
    if the given student is whitelisted.
    """
    try:
        white_list_certificate = CertificateWhitelist.get_certificate_white_list(course.id, student)
        if white_list_certificate:
            course_enrollment_obj = CourseEnrollment.get_enrollment(student, course.id)
            if course_enrollment_obj:
                course_enrollment_obj.change_mode(CourseMode.VERIFIED)
    except Exception as e:  # pylint: disable=broad-except
        LOG.exception(str(e))
