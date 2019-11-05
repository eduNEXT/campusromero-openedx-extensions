"""
Storage backend for certificates QR codes.
"""
from __future__ import absolute_import

import StringIO

import qrcode
from django.conf import settings
from django.core.files.storage import get_storage_class
from django.core.files.uploadedfile import InMemoryUploadedFile
from storages.backends.s3boto import S3BotoStorage
from storages.utils import setting


class CertificatesQRCodeS3Storage(S3BotoStorage):  # pylint: disable=abstract-method
    """
    S3 backend for course import and export OLX files.
    """

    def __init__(self):
        bucket = setting('CERTIFICATES_QR_CODE_BUCKET',
                         settings.AWS_STORAGE_BUCKET_NAME)
        super(CertificatesQRCodeS3Storage, self).__init__(
            bucket=bucket,
            custom_domain=None,
            querystring_auth=False,
            acl='public-read'
        )


# pylint: disable=invalid-name
certificates_qr_code_storage = get_storage_class(settings.CERTIFICATES_QR_CODE_STORAGE)()


def generateQr(url, certificate_id_number):
    """
    Generate QR used in the certificates.
    """
    try:
        img_filename = 'qr{}.png'.format(certificate_id_number)
        if not certificates_qr_code_storage.exists(img_filename):
            img = qrcode.make(url)
            img_io = StringIO.StringIO()
            img.save(img_io, format='PNG')
            django_file = InMemoryUploadedFile(
                img_io, None, img_filename, 'image/png', img_io.len, None
            )
            certificates_qr_code_storage.save(
                img_filename, django_file
            )
        qrcode_s3_url = certificates_qr_code_storage.url(img_filename)
        return qrcode_s3_url
    except Exception as e:
        return ''
