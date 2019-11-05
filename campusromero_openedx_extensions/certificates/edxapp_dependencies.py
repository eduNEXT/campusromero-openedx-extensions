"""
Module to import edx platform dependencies.
"""
from course_modes.models import CourseMode  # pylint: disable=import-error
from lms.djangoapps.certificates.models import CertificateWhitelist  # pylint: disable=import-error
from student.models import CourseEnrollment  # pylint: disable=import-error
