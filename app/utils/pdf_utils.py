from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
from io import BytesIO
import qrcode
from schemas.area_imovel_projeto_schema import PlusCode


def gerar_pdf_bytes(info_pluscode: PlusCode):

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Título
    c.translate(inch,inch)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(72, height - 172, "Certificado de Endereço Digital")

    # Texto (você pode ajustar posições/tamanhos)
    c.setFont("Helvetica", 12)
    """
    Certificado de Endereço Digital
    Este certificado atesta a existência e a exatidão do endereço digital associado ao imóvel a seguir.
    """
    c.drawString(72, height - 220, f"Certificado de Endereço Digital")
    c.drawString(72, height - 250, f"Este certificado atesta a existência e a exatidão do endereço digital associado ao imóvel a seguir.")
    c.drawString(72, height - 320, f"Proprietário: {info_pluscode.owner_name}")
    c.drawString(72, height - 340, f"Imóvel (CAR/ID): {info_pluscode.cod_imovel}")
    c.drawString(72, height - 360, f"Plus Code: {info_pluscode.pluscode_cod}")
    c.drawString(72, height - 380, f"Coordenadas: {info_pluscode.cordinates}")
    c.drawString(72, height - 400, f"Data/Hora (UTC): {info_pluscode.validation_date}")
    c.drawString(72, height - 420, f"Hash de Validação: {info_pluscode.id}")
    
    # Linhas 
    c.line(0,0,0,10*inch)
    c.line(0,0,7*inch,0)
    c.setStrokeColorRGB(0.2,0.5,0.3)


    # QR Code com infos (imovel|plus|hash)
    qr_payload = f"{info_pluscode.cod_imovel}|{info_pluscode.pluscode_cod}|{info_pluscode.id}"
    qr = qrcode.make(qr_payload)
    qr_buffer = BytesIO()
    qr.save(qr_buffer, format="PNG")
    # qr_buffer.seek(0)
    img = ImageReader(qr_buffer)

    # Mostrar QR code
    c.drawImage(img, width - 160, height - 700, width=120, height=120)

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer.read(), info_pluscode.id