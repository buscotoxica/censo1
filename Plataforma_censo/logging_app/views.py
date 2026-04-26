import json
import re
import time
import imaplib
import email as email_lib
import smtplib
import datetime
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.cache import cache
from .models import RegistroAcceso, CorreoBloqueado, IPBloqueada


def get_client_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


@csrf_exempt
def registrar_click(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            RegistroAcceso.objects.create(
                email=data.get("email"),
                panel=data.get("panel"),
                tipo="acceso"
            )
            return JsonResponse({"status": "ok"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def verificar_email(request):
    if request.method != 'POST':
        return JsonResponse({'valid': False})

    try:
        data = json.loads(request.body)
        email_dest = data.get('email', '').strip().lower()
    except:
        return JsonResponse({'valid': False})

    ip = get_client_ip(request)

    # Verificar si IP está bloqueada
    try:
        bloqueo = IPBloqueada.objects.get(ip=ip)
        if bloqueo.permanente:
            return JsonResponse({
                'valid': False,
                'error': 'Acceso bloqueado permanentemente. Contacte al administrador: trabajossig@munivalpo.cl',
                'bloqueado': True,
                'permanente': True
            })
        elif bloqueo.hasta and bloqueo.hasta > timezone.now():
            tiempo_restante = bloqueo.hasta - timezone.now()
            horas = int(tiempo_restante.total_seconds() // 3600)
            minutos = int((tiempo_restante.total_seconds() % 3600) // 60)
            return JsonResponse({
                'valid': False,
                'error': f'Acceso bloqueado. Intente en {horas}h {minutos}min.',
                'bloqueado': True,
                'permanente': False
            })
    except IPBloqueada.DoesNotExist:
        pass

    if not re.match(r'^[a-zA-Z0-9._%+\-]+@munivalpo\.cl$', email_dest):
        return JsonResponse({'valid': False, 'error': 'Solo correos @munivalpo.cl'})

    # Guardar como pendiente en cache
    cache.set(f'email_status_{email_dest}', 'pendiente', timeout=120)

    # Verificar en background
    def verificar_en_background(email_dest, ip):
        try:
            asunto_unico = f'VERIFY-{int(time.time())}'
            msg = MIMEText('Verificación de correo institucional.')
            msg['Subject'] = asunto_unico
            msg['From'] = 'trabajossig@munivalpo.cl'
            msg['To'] = email_dest

            server = smtplib.SMTP('mail.munivalpo.cl', 587, timeout=10)
            server.starttls()
            server.login(r'servervalpo\trabajossig', 'Practica_2024')
            server.sendmail('trabajossig@munivalpo.cl', [email_dest], msg.as_string())
            server.quit()

            print(f"Correo enviado a {email_dest}, esperando rebote...")
            time.sleep(50)

            mail = imaplib.IMAP4_SSL('mail.munivalpo.cl', 993)
            mail.login(r'servervalpo\trabajossig', 'Practica_2024')
            mail.select('INBOX')

            status, messages = mail.search(None, f'(SUBJECT "{asunto_unico}")')
            if not (status == 'OK' and messages[0]):
                status, messages = mail.search(None, 'UNSEEN SUBJECT "Delivery has failed"')
            if not (status == 'OK' and messages[0]):
                status, messages = mail.search(None, 'UNSEEN SUBJECT "Undeliverable"')

            rebote_encontrado = False
            if status == 'OK' and messages[0]:
                ids = messages[0].split()
                for num in ids:
                    status2, data2 = mail.fetch(num, '(RFC822)')
                    raw = data2[0][1]
                    msg_recibido = email_lib.message_from_bytes(raw)
                    remitente = msg_recibido.get('From', '')
                    if any(x in remitente.lower() for x in ['mailer-daemon', 'postmaster', 'undeliverable', 'delivery', 'microsoft outlook']):
                        rebote_encontrado = True
                        mail.store(num, '+FLAGS', '\\Deleted')
                        break

            mail.expunge()
            mail.logout()

            if rebote_encontrado:
                print(f"REBOTE detectado para {email_dest} - BLOQUEADO")

                # Registrar intento fallido
                CorreoBloqueado.objects.create(email=email_dest, ip=ip)

                # Contar intentos en últimos 30 minutos
                hace_30min = timezone.now() - datetime.timedelta(minutes=30)
                intentos_recientes = CorreoBloqueado.objects.filter(
                    ip=ip,
                    fecha__gte=hace_30min
                ).count()

                print(f"IP {ip} tiene {intentos_recientes} intentos fallidos en últimos 30 min")

                if intentos_recientes >= 2:
                    bloqueo_existente = IPBloqueada.objects.filter(ip=ip).first()

                    if bloqueo_existente:
                        # Ya fue bloqueada antes → permanente
                        bloqueo_existente.permanente = True
                        bloqueo_existente.bloqueos += 1
                        bloqueo_existente.hasta = None
                        bloqueo_existente.save()
                        print(f"IP {ip} BLOQUEADA PERMANENTEMENTE")
                        cache.set(f'email_status_{email_dest}', 'bloqueado_permanente', timeout=3600)
                    else:
                        # Primera vez → 24 horas
                        IPBloqueada.objects.create(
                            ip=ip,
                            hasta=timezone.now() + datetime.timedelta(hours=24),
                            permanente=False,
                            bloqueos=1
                        )
                        print(f"IP {ip} BLOQUEADA 24 HORAS")
                        cache.set(f'email_status_{email_dest}', 'bloqueado_24h', timeout=3600)
                else:
                    cache.set(f'email_status_{email_dest}', 'invalido', timeout=3600)
            else:
                print(f"Sin rebote para {email_dest} - VÁLIDO")
                cache.set(f'email_status_{email_dest}', 'valido', timeout=3600)

        except Exception as e:
            print(f"ERROR verificación background: {str(e)}")
            cache.set(f'email_status_{email_dest}', 'valido', timeout=3600)

    t = threading.Thread(target=verificar_en_background, args=(email_dest, ip))
    t.daemon = True
    t.start()

    return JsonResponse({'valid': True})


@csrf_exempt
def estado_email(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error'})
    try:
        data = json.loads(request.body)
        email_dest = data.get('email', '').strip().lower()
        status = cache.get(f'email_status_{email_dest}', 'pendiente')
        return JsonResponse({'status': status})
    except Exception as e:
        return JsonResponse({'status': 'error'})


@csrf_exempt
def enviar_comprobante(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error'})

    try:
        data = json.loads(request.body)
        email = data.get('email', '')
        modo = data.get('modo', '')
        annio = data.get('annio', '')
        metricas = data.get('metricas', [])
        seleccion = data.get('seleccion', '')

        ahora = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
        modos = {'uv': 'Unidad Vecinal (UV)', 'sb': 'Sector Barrial (SB)', 'omz': 'OMZ', 'cm': 'Comunal'}
        modo_label = modos.get(modo, modo.upper())
        metricas_fmt = ', '.join([m.replace('_', ' ').title() for m in metricas[:10]])
        if len(metricas) > 10:
            metricas_fmt += f' y {len(metricas)-10} más'

        mi_correo = 'trabajossig@munivalpo.cl'
        asunto = 'Comprobante de consulta — Plataforma SIG Valparaíso'

        mensaje = MIMEMultipart()
        mensaje['From'] = mi_correo
        mensaje['To'] = email
        mensaje['Subject'] = asunto

        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #1a2a3a;">
            <p>Estimado/a usuario/a,</p>
            <p>Usted ha realizado una consulta en la <strong>Plataforma SIG Valparaíso</strong>.</p>
            <hr style="border: 1px solid #e2e8f0;">
            <table style="font-size:14px;">
                <tr><td style="padding:4px 12px 4px 0;color:#64748b;">Fecha y hora</td><td><strong>{ahora}</strong></td></tr>
                <tr><td style="padding:4px 12px 4px 0;color:#64748b;">Tipo</td><td><strong>{modo_label}</strong></td></tr>
                <tr><td style="padding:4px 12px 4px 0;color:#64748b;">Selección</td><td><strong>{seleccion}</strong></td></tr>
                <tr><td style="padding:4px 12px 4px 0;color:#64748b;">Año censo</td><td><strong>{annio}</strong></td></tr>
                <tr><td style="padding:4px 12px 4px 0;color:#64748b;">Variables</td><td><strong>{metricas_fmt}</strong></td></tr>
            </table>
            <hr style="border: 1px solid #e2e8f0;">
            <p style="font-size:12px;color:#94a3b8;">Este es un mensaje automático, por favor no responda este correo.</p>
            <p style="font-size:12px;color:#94a3b8;">Departamento SIG · Municipalidad de Valparaíso</p>
        </body>
        </html>
        """

        mensaje.attach(MIMEText(html_content, 'html'))

        print(f"=== ENVIANDO EMAIL A: {email} ===")
        server = smtplib.SMTP('mail.munivalpo.cl', 587)
        server.starttls()
        server.login(r'servervalpo\trabajossig', 'Practica_2024')
        server.sendmail(mi_correo, [email], mensaje.as_string())
        server.quit()
        print("=== EMAIL ENVIADO OK ===")

        return JsonResponse({'status': 'ok'})

    except Exception as e:
        print(f"=== ERROR EMAIL: {str(e)} ===")
        return JsonResponse({'status': 'error', 'msg': str(e)})