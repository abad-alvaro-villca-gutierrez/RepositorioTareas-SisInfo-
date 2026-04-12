import smtplib
from email.message import EmailMessage
import sys
import os
from dotenv import load_dotenv

# Cargamos las variables del archivo .env al sistema
load_dotenv() 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.conexion_bd import traer_tareas_vencidas

def enviar_reporte_docente(correo_destino):
    # 1. Obtener los datos de la Base de Datos
    tareas = traer_tareas_vencidas()
    
    if not tareas:
        print("ℹ️ No hay tareas vencidas para reportar.")
        return False

    # 2. Leemos las credenciales de forma segura
    remitente = os.getenv("CORREO_SISTEMA")
    password = os.getenv("PASSWORD_CORREO")

    # Filtro de seguridad: verificamos que sí encontró el .env
    if not remitente or not password:
        print("❌ Error: Faltan credenciales en el archivo .env")
        return False

    # 3. Construir el esqueleto del correo
    msg = EmailMessage()
    msg['Subject'] = "Reporte Automático: Tareas Vencidas en el Sistema"
    msg['From'] = remitente
    msg['To'] = correo_destino
    
    # 4. Estructurar el reporte en HTML
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body style="font-family: 'Segoe UI', Arial, sans-serif; background-color: #F5F1E8; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #FFFFFF; padding: 30px; border-radius: 8px; border-top: 5px solid #FF5252;">
            <h2 style="color: #6D4145; margin-top: 0;">Resumen del Sistema</h2>
            <p style="color: #555555; font-size: 14px;">
                Hola Docente, <br><br>
                Este es un reporte automático generado por el <b>Sistema de Gestión de Tareas</b>. 
                Las siguientes tareas han superado su fecha límite y continúan con estado "Publicada":
            </p>
            
            <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                <thead>
                    <tr style="background-color: #6D4145; color: #FFEFAE; text-align: left;">
                        <th style="padding: 12px; border: 1px solid #ddd;">Nombre de la Tarea</th>
                        <th style="padding: 12px; border: 1px solid #ddd;">Fecha de Vencimiento</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    # 5. Rellenar la tabla dinámicamente con los datos
    for t in tareas:
        nombre = t[0]
        # Formateamos la fecha si es un objeto datetime, si no, se imprime como viene
        fecha_vence = t[1].strftime("%d/%m/%Y") if hasattr(t[1], 'strftime') else t[1] 
        
        html_content += f"""
                    <tr>
                        <td style="padding: 10px; border: 1px solid #ddd; color: #333;">{nombre}</td>
                        <td style="padding: 10px; border: 1px solid #ddd; color: #C62828; font-weight: bold;">{fecha_vence}</td>
                    </tr>
        """

    # Cerramos el HTML
    html_content += """
                </tbody>
            </table>
            
            <p style="color: #777; font-size: 12px; margin-top: 30px; text-align: center;">
                Por favor, ingresa a tu panel de control para calificar o cerrar estas tareas.<br>
                <i>No respondas a este correo.</i>
            </p>
        </div>
    </body>
    </html>
    """

    # Adjuntamos el HTML al mensaje
    msg.add_alternative(html_content, subtype='html')
    
    # 6. Conectar al servidor y enviar
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(remitente, password) 
            smtp.send_message(msg)
            
        print("✅ Reporte enviado con éxito al correo del docente.")
        return True
    except Exception as e:
        print(f"❌ Error al enviar el correo: {e}")
        return False