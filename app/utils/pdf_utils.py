from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
import qrcode
from schemas.area_imovel_projeto_schema import PlusCode


def gerar_pdf_bytes(info_pluscode: PlusCode):

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Título
    c.setFont("Helvetica-Bold", 18)
    c.drawString(72, height - 72, "Certificado de Endereço Digital")

    # Texto (você pode ajustar posições/tamanhos)
    c.setFont("Helvetica", 12)
    c.drawString(72, height - 120, f"Proprietário: {info_pluscode.owner_name}")
    c.drawString(72, height - 140, f"Imóvel (CAR/ID): {info_pluscode.cod_imovel}")
    c.drawString(72, height - 160, f"Plus Code: {info_pluscode.pluscode_cod}")
    c.drawString(72, height - 180, f"Coordenadas: {info_pluscode.cordinates}")
    c.drawString(72, height - 200, f"Data/Hora (UTC): {info_pluscode.validation_date}")
    c.drawString(72, height - 220, f"Hash de Validação: {info_pluscode.id}")

    # QR Code com infos (imovel|plus|hash)
    qr_payload = f"{info_pluscode.cod_imovel}|{info_pluscode.pluscode_cod}|{info_pluscode.id}"
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
    return buffer.read(), info_pluscode.id