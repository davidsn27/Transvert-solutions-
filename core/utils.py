import os
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generar_etiqueta_envio(envio):
    carpeta = "media/etiquetas"
    os.makedirs(carpeta, exist_ok=True)

    ruta_pdf = f"{carpeta}/guia_{envio.numero_guia}.pdf"

    c = canvas.Canvas(ruta_pdf, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 770, "TRANSVERT SOLUTIONS")

    c.setFont("Helvetica", 12)
    c.drawString(50, 735, f"GUÍA: {envio.numero_guia}")

    c.drawString(50, 705, f"Remitente: {envio.remitente_nombre}")
    c.drawString(50, 685, f"Teléfono: {envio.remitente_telefono}")

    c.drawString(50, 655, f"Destinatario: {envio.destinatario_nombre}")
    c.drawString(50, 635, f"Teléfono: {envio.destinatario_telefono}")

    c.drawString(50, 605, f"Tipo envío: {envio.tipo_envio}")
    c.drawString(50, 585, f"Peso: {envio.peso} Kg")
    c.drawString(50, 565, f"Dimensiones: {envio.dimensiones}")

    c.drawString(50, 535, f"Origen: {envio.direccion_origen}")
    c.drawString(50, 515, f"Destino: {envio.direccion_destino}")

    c.drawString(50, 485, f"Estado: {envio.estado}")
    c.drawString(50, 465, f"Fecha: {envio.fecha_creado.strftime('%d/%m/%Y')}")

    # ✅ QR
    qr = qrcode.make(envio.numero_guia)
    ruta_qr = f"{carpeta}/qr_{envio.numero_guia}.png"
    qr.save(ruta_qr)

    c.drawImage(ruta_qr, 350, 540, width=150, height=150)

    c.rect(40, 450, 520, 330)  # Marco de etiqueta

    c.showPage()
    c.save()

    return ruta_pdf
