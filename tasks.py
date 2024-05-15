from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Empleado
import datetime

@shared_task
def pagar_nominas():
    # Obtén la lista de empleados
    empleados = Empleado.objects.all()

    for empleado in empleados:
        # Genera el desprendible de pago y envía el correo
        generar_y_enviar_desprendible(empleado)

def generar_y_enviar_desprendible(empleado):
    # Lógica para generar el desprendible de pago en PDF
    # Guarda el PDF en S3 y envía el correo electrónico con el archivo adjunto
    pass

@shared_task
def send_email(subject, message, recipient_list, from_email=settings.DEFAULT_FROM_EMAIL):
    send_mail(subject, message, from_email, recipient_list)


