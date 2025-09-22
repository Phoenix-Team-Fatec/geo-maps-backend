from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
import qrcode
from datetime import datetime
import hashlib

# def gerar_hash(imovel_id: str, plus_code: str, timestamp: str) -> str:
#     raw = f"{imovel_id}|{plus_code}|{timestamp}"
#     return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def gerar_pdf_bytes(nome: str, imovel_id: str, plus_code: str, coordenadas: str):
    ts = datetime.utcnow().isoformat()
    hash_id = gerar_hash(imovel_id, plus_code, ts)

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Título
    c.setFont("Helvetica-Bold", 18)
    c.drawString(72, height - 72, "Certificado de Endereço Digital")

    # Texto (você pode ajustar posições/tamanhos)
    c.setFont("Helvetica", 12)
    c.drawString(72, height - 120, f"Proprietário: {nome}")
    c.drawString(72, height - 140, f"Imóvel (CAR/ID): {imovel_id}")
    c.drawString(72, height - 160, f"Plus Code: {plus_code}")
    c.drawString(72, height - 180, f"Coordenadas: {coordenadas}")
    c.drawString(72, height - 200, f"Data/Hora (UTC): {ts}")
    c.drawString(72, height - 220, f"Hash de Validação: {hash_id}")

    # QR Code com infos (imovel|plus|hash)
    qr_payload = f"{imovel_id}|{plus_code}|{hash_id}"
    qr = qrcode.make(qr_payload)
    qr_buffer = BytesIO()
    qr.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)
    img = ImageReader(qr_buffer)

    # Mostrar QR code
    c.drawImage(img, width - 160, height - 260, width=120, height=120)

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer.read(), hash_id