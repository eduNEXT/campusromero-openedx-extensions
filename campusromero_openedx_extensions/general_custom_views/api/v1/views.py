"""
Views for the camrom api.
"""
import uuid

from rest_framework import status
from rest_framework import permissions

from rest_framework.views import APIView

from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication  # pylint: disable=import-error,line-too-long

from django.http import JsonResponse
from django.contrib.auth.models import User

from campusromero_openedx_extensions.edxapp_wrapper.verify_student import get_software_photo_verification

SoftwareSecurePhotoVerification = get_software_photo_verification()


class ChangeToVerifiedMode(APIView):
    """
    Change the status to 'approved' in Software Secure Photo Verification model for the given user.
    """
    authentication_classes = (JwtAuthentication,)
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    def post(self, request):
        """
        Change the status of the user into Software Secure Photo Verification model,
        if it not exist, is created instead with status value 'approved' by default.
        Receive a username key, with the username value to change status.
        POST api/user/v1/preferences/change_to_verified_mode/
        Returns:
            Json object that contains two keys: status and username.
            - status: Inidicate the operation status, created, updated or user does not exist error.
            - username: Contains the username provided in post request.
        """
        if not request.data.get('username'):
            return JsonResponse({
                'status': 'No username key provided.',
                'username': ''
            }, status=status.HTTP_400_BAD_REQUEST)

        username = request.data['username']
        operation_status = 'updated'
        try:
            user_info = User.objects.get(username=username)  # pylint: disable=no-member
        except User.DoesNotExist:  # pylint: disable=no-member
            return JsonResponse({
                'status': 'The user with username: {}, does not exist.'.format(username),
                'username': username
            }, status=status.HTTP_404_NOT_FOUND)
        try:
            user_photo_verification = SoftwareSecurePhotoVerification.objects.get(
                user_id=user_info.id)
            user_photo_verification.status = 'approved'
            user_photo_verification.save()
        except SoftwareSecurePhotoVerification.DoesNotExist:
            operation_status = 'created'
            receipt_id = str(uuid.uuid4())
            user_photo_verification = SoftwareSecurePhotoVerification(
                status='approved',
                receipt_id=receipt_id,
                user_id=user_info.id
            )
            user_photo_verification.save()
        return JsonResponse({
            'status': operation_status,
            'username': username
        }, status=status.HTTP_200_OK)
