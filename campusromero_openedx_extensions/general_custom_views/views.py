# -*- coding: utf-8 -*-
import datetime
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.db import transaction
from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_exempt

from opaque_keys.edx.keys import CourseKey  # pylint: disable=import-error
from opaque_keys.edx.locations import SlashSeparatedCourseKey  # pylint: disable=import-error

from course_modes.models import CourseMode  # pylint: disable=import-error

from student.models import UserProfile, CourseEnrollment  # pylint: disable=import-error
from xmodule.modulestore.django import modulestore  # pylint: disable=import-error
from util.db import outer_atomic

from campusromero_openedx_extensions.edxapp_wrapper.edxmako_module import render_to_response

LOG = logging.getLogger("edx.student")
EMAIL_TEMPLATE = "<table border=0 cellpadding=0 cellspacing=0 style=font-family:Arial,Helvetica,sans-serif;font-size:12px;color:#585858;width:650px align=center width=650><tr><td height=10 valign=middle align=left> <tr><td valign=top style=background-color:#dbf2ff><table border=0 cellpadding=0 cellspacing=0 style=width:648px><tr><td height=10 width=3%> <td height=10 width=94%> <td height=10 width=3%> <tr><td width=3%> <td width=94% style=font-family:Arial,Helvetica,sans-serif;font-size:24px;color:#db5008><strong>Formulario Contáctanos</strong><td width=3%> <tr><td height=10> <td height=10 valign=top> <td height=10> <tr><td> <td valign=top><p style=font-family:Arial,Helvetica,sans-serif;font-size:12px;color:#585858;line-height:16px>Estimado administrador <strong></strong>:<br><br>Se registró el siguiente formulario para su revisión:<br><p style=font-family:Arial,Helvetica,sans-serif;font-size:12px;color:#585858;line-height:16px>Nombre completo:<strong>{nombreCompleto}</strong><p style=font-family:Arial,Helvetica,sans-serif;font-size:12px;color:#585858;line-height:16px>Email:<strong>{email}</strong><p style=font-family:Arial,Helvetica,sans-serif;font-size:12px;color:#585858;line-height:16px>Región:<strong>{region}</strong><p style=font-family:Arial,Helvetica,sans-serif;font-size:12px;color:#585858;line-height:16px>Curso:<strong>{curso}</strong><p style=font-family:Arial,Helvetica,sans-serif;font-size:12px;color:#585858;line-height:16px>Teléfono:<strong>{telefono}</strong><p style=font-family:Arial,Helvetica,sans-serif;font-size:12px;color:#585858;line-height:16px>Tema:<strong>{tema}</strong><p style=font-family:Arial,Helvetica,sans-serif;font-size:12px;color:#585858;line-height:16px><strong></strong>Descripción:<br><strong>{descripcion}</strong><p><br><td> <tr><td height=10> <td height=10> <td height=10> </table><tr><td style=background-color:#0087ce><table border=0 cellpadding=0 cellspacing=0 style=width:648px><tr><td height=10> <td height=10> <td height=10> <td height=10> <tr><td width=3%> <td width=47% align=left valign=top><p style=font-family:Arial,Helvetica,sans-serif;font-size:11px;color:#fff;line-height:14px><td width=47% align=right valign=top><p style=font-family:Arial,Helvetica,sans-serif;font-size:11px;color:#fff;line-height:14px><strong>Campus Romero</strong><br><a href=https://www.campusromero.pe target=_blank style=font-family:Arial,Helvetica,sans-serif;font-size:11px;color:#fff;line-height:14px;text-decoration:none>www.campusromero.pe</a><td width=3%> <tr><td height=10> <td height=10> <td height=10> <td height=10> </table>"  # pylint: disable=line-too-long


# ITSoluciones
@xframe_options_exempt
def iframe_log_reg(request):
    user = request.user
    context = {
        'user': user,
        'lms_root_url': settings.LMS_ROOT_URL
    }
    return render_to_response('general_custom_views/iframe_login.html', context)


# ITSoluciones
@xframe_options_exempt
def purchase_course(request, course_id):
    user = request.user
    p_course = course_id
    bool_ac = False
    bool_in = False
    syserror = ''

    # 1.Datos basicos del curso si existe
    # NOTE: definitively the logic below deserves to be refactored, but for now left as it is
    try:
        course_id = SlashSeparatedCourseKey.from_deprecated_string(p_course)
        course = modulestore().get_course(course_id)
        student_enrolled = CourseEnrollment.is_enrolled(request.user, course_id)
        analytics = p_course.split("+")[1]

        import pytz
        lima = pytz.timezone("America/Lima")
        date_time = lima.localize(datetime.datetime.now())

        if course.start.date() == date_time.date():
            if course.start.time() >= date_time.time():
                bool_ac = True
        elif course.start.date() > date_time.date():
            bool_ac = True

        if not course.enrollment_start or not course.enrollment_end:
            if not course.enrollment_end:
                if date_time.date() == course.end.date():
                    if date_time.time() <= course.end.time():
                        bool_in = True
                elif date_time.date() < course.end.date():
                    bool_in = True
            elif not course.enrollment_start:
                if date_time.date() == course.enrollment_end.date():
                    if date_time.time() <= course.enrollment_end.time():
                        bool_in = True
                elif date_time.date() < course.enrollment_end.date():
                    bool_in = True

        else:
            if course.enrollment_start.date() == date_time.date():
                if course.enrollment_start.time() <= date_time.time():
                    if course.enrollment_end.date() > date_time.date():
                        bool_in = True
                    if course.enrollment_end.date() == date_time.date():
                        if course.enrollment_end.time() > date_time.time():
                            bool_in = True
            elif course.enrollment_start.date() < date_time.date():
                if course.enrollment_end.date() > date_time.date():
                    bool_in = True
                if course.enrollment_end.date() == date_time.date():
                    if course.enrollment_end.time() > date_time.time():
                        bool_in = True
    except Exception as e:
        context = {
            'error': "CURSO NO EXISTENTE",
            'exception': e,
            'user': user,
            'cod_course': p_course
        }
        return render_to_response('general_custom_views/purchase_course.html', context)

    # 2.Verificar si el curso esta abierto
    if not bool_in and not student_enrolled:
        context = {
            'error': "INSCRIPCION CERRADA",
            'user': user,
            'cod_course': p_course
        }
        return render_to_response('general_custom_views/purchase_course.html', context)
    sku = ""
    # 3.Obtener datos si es examen

    # Magia Digital - VD, integracion con el e-commerce
    # modalidad de curso no-id-professional va directamente al ecommerce
    # modalidad audit o verified lleva a la pantalla de eleccion
    try:

        CourseDict = CourseMode.modes_for_course_dict(course_id)

        for key in CourseDict.keys():
            if key == 'no-id-professional':
                sku = CourseMode.modes_for_course_dict(course_id)[key].sku
                price = CourseMode.modes_for_course_dict(course_id)[key].min_price
                exp_date = CourseMode.modes_for_course_dict(course_id)[key].expiration_datetime
                is_payment = CourseMode.objects.filter(course_id=course_id).exists()

                if exp_date:
                    exp_date = exp_date.strftime("%d/%m/%Y")
            else:
                price = None
                exp_date = None
                is_payment = None
    except KeyError as e:
        price = None
        exp_date = None
        is_payment = None
        syserror = CourseMode.modes_for_course_dict(course_id)
    # 4.Obtener datos del usuario
    user = request.user
    if not user.is_authenticated():
        user_p = ''
    else:
        user_p = UserProfile.objects.get(user=request.user)

    # 5.Logica de inscripcion
    # cursos_gr = None
    is_course_payment = is_payment and price > 0
    context = {
        "cod_course": p_course,
        "analytics": analytics,
        "student_enrolled": student_enrolled,
        "ins": bool_in,
        "user": user,
        "price": price,
        "user_p": user_p,
        "still_start": bool_ac,
        "exp_date": exp_date,
        "is_payment": is_payment,
        "is_course_payment": is_course_payment,
        "sku": sku,
        "syserror": syserror,
        "ecommerce_public_url_root": settings.ECOMMERCE_PUBLIC_URL_ROOT
    }

    return render_to_response('general_custom_views/purchase_course.html', context)


@transaction.non_atomic_requests
@require_POST
@outer_atomic(read_committed=True)
def change_enrollment(request, course_id, check_access=True):

    if not request.user.is_authenticated:
        return HttpResponse("An authenticated user is required", status=401)

    try:
        CourseEnrollment.enroll(request.user, CourseKey.from_string(course_id))
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(str(e), status=500)


def noLoginBasket(request, sku):
    path_basket = "/basket/add/?sku=" + sku
    return redirect(settings.ECOMMERCE_PUBLIC_URL_ROOT + path_basket)


def noLogingVerified(request, course_id):

    if not request.user.is_authenticated:
        return HttpResponse("An authenticated user is required", status=401)

    try:
        CourseEnrollment.enroll(request.user, CourseKey.from_string(course_id))
        path_course_mode_choose = reverse(
            'course_modes_choose',
            kwargs={'course_id': course_id}
        )
        return HttpResponseRedirect(settings.LMS_ROOT_URL + path_course_mode_choose)
    except Exception as e:
        return HttpResponse(str(e), status=500)


def enviarMail(mail, body, name):

    # Configuracion de inicio
    '''
    SMTPserver = 'mail.magiadigital.com'
    USERNAME = 'envios'
    PASSWORD = 'env10s'
    '''
    SMTPserver = settings.EMAIL_HOST
    USERNAME = settings.EMAIL_HOST_USER
    PASSWORD = settings.EMAIL_HOST_PASSWORD
    WEBMASTER = settings.CONTACT_EMAIL

    # Variables de inicio

    sender = WEBMASTER
    receiver = WEBMASTER  # 'dramos@magiadigital.com'
    msg = MIMEMultipart()

    msg['From'] = name + '<' + mail + '>'
    msg['to'] = receiver

    html = MIMEText(body, 'html', _charset='utf-8')
    msg.attach(html)
    msg['Subject'] = ("Formulario de contáctanos")

    # Envio del mensaje
    conn = smtplib.SMTP(SMTPserver)
    conn.set_debuglevel(False)
    conn.login(USERNAME, PASSWORD)

    try:
        conn.sendmail(sender, receiver, msg.as_string())
        LOG.info("---------------------->ENVIADO<------------------------")

        return True
    except Exception as e:
        LOG.info(e)
        return False
    finally:
        conn.quit()


class contactanos(APIView):
    '''
    {
       "usuario":{
          "nombreCompleto":"APPROVED",
          "email":"dramos@magiadigital.com",
          "region":"Perú",
          "curso":"Rocket fuel",
          "telefono":"978725447",
          "tema":"Composición química",
          "descripcion":"¿Cómo puedo hacer para que la combustión propagada por la explosión
                         no pueda ser apagada facilmente"
       }
    }
    '''
    def post(self, request):

        log.info("---------------------->CONFIRMADO<------------------------")
        data = request.data.get('usuario', {})
        nombreCompleto = data.get('nombreCompleto', '')
        email = data.get('email', '')
        region = data.get('region', '')
        curso = data.get('curso', '')
        telefono = data.get('telefono', '')
        tema = data.get('tema', '')
        descripcion = data.get('descripcion', '')

        body = EMAIL_TEMPLATE.replace(
            '{nombreCompleto}',
            nombreCompleto.encode('utf-8')
        ).replace(
            '{email}',
            email.encode('utf-8')
        ).replace(
            '{region}',
            region.encode('utf-8')
        ).replace(
            '{curso}',
            curso.encode('utf-8')
        ).replace(
            '{telefono}',
            telefono.encode('utf-8')
        ).replace(
            '{tema}',
            tema.encode('utf-8')
        ).replace(
            '{descripcion}',
            descripcion.encode('utf-8')
        )

        enviarMail(email, str(body), nombreCompleto)

        return Response(
            status=status.HTTP_200_OK,
            data={
                "message": "Confirmado",
                "data": data
            },
            headers={'Access-Control-Allow-Origin': '*'},
        )
