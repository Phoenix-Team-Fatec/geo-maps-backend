from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
#from reportlab.pdfbase.pdfmetrics import stringWidth 
from io import BytesIO
import qrcode
from app.schemas.area_imovel_projeto_schema import PlusCode
import os


def gerar_pdf_bytes(info_pluscode: PlusCode, user_info: dict):
    """
    Colocar informações do usuário no PDF,
    Informações:
    
    info_pluscode:
            - email
    
    user_info:
            - cpf
            - nome 
            - sobrenome 
    """



    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    # Definir margem padrão
    margin = 40

    # Logo 
    logo_path = os.path.join("assets", "geomaps_logo.jpg")
    if os.path.exists(logo_path):
        c.drawImage(logo_path, width/2 - 60, height - 140, width=120, height=60, preserveAspectRatio=True, mask='auto')


    # Título
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width/2, height - 180, "CERTIFICADO DE ENDEREÇO DIGITAL")

    # Subtítulo
    c.setFont("Helvetica-Oblique", 12)
    c.drawCentredString(width/2, height - 200, "Documento oficial de validação de localização digital")

    #  Texto principal
    y = height - 260
    c.setFont("Helvetica", 12)
   
   # Texto introdutório
    c.setFont("Helvetica", 12)
    c.drawString(80, y, "Este certificado atesta a existência e a exatidão do endereço digital associado ao")
    y -= 15
    c.drawString(80, y, "imóvel a seguir.")
    y -= 30

        # Nome do proprietário e infos usuários
    c.setFont("Helvetica-Bold", 12)
    c.drawString(80, y, "Nome do proprietário: ")
    # Nome
    c.setFont("Helvetica-Bold", 12)
    c.drawString(80, y, "Nome do proprietário: ")
    c.setFont("Helvetica", 12)
    c.drawString(
        250, y, f"{user_info.get('nome', '')} {user_info.get('sobrenome', '')}"
    )
    y -= 20

    # CPF
    c.setFont("Helvetica-Bold", 12)
    c.drawString(80, y, "CPF do proprietário: ")
    c.setFont("Helvetica", 12)
    c.drawString(250, y, f"{user_info.get('cpf', '')}")
    y -= 20

    # Email
    c.setFont("Helvetica-Bold", 12)
    c.drawString(80, y, "E-mail do proprietário: ")
    c.setFont("Helvetica", 12)
    c.drawString(250, y, f"{info_pluscode.owner_email}")
    y -= 30

    c.setFont("Helvetica-Bold", 12)
    c.drawString(80, y, "Identificação do imóvel: ")
    c.setFont("Helvetica", 12)
    c.drawString(250, y, f"{info_pluscode.cod_imovel}")
    y -= 20

    c.setFont("Helvetica-Bold", 12)
    c.drawString(80, y, "Plus Code: ")
    c.setFont("Helvetica", 12)
    c.drawString(250, y, f"{info_pluscode.pluscode_cod}")
    y -= 30

    c.setFont("Helvetica-Bold", 12)
    c.drawString(80, y, "Coordenadas Geográficas: ")
    y -= 20
    c.setFont("Helvetica", 12)
    c.drawString(120, y, f"{info_pluscode.cordinates}")
    y -= 30

    c.setFont("Helvetica-Bold", 12)
    c.drawString(80, y, "Data e Hora da Validação: ")
    c.setFont("Helvetica", 12)
    c.drawString(250, y, f"{info_pluscode.validation_date}")
    y -= 20

    c.setFont("Helvetica-Bold", 12)
    c.drawString(80, y, "Hash/ID de Validação: ")
    c.setFont("Helvetica", 12)
    c.drawString(250, y, f"{info_pluscode.id}")
    y -= 40
    
    # Texto final
    c.setFont("Helvetica", 11)
    c.drawString(80, y, "Este documento comprova a autenticidade das informações de localização no momento da ")
    y -= 15 #quebra de linha manual 
    c.drawString(80, y, "emissão, sendo uma ferramenta para validação e rastreabilidade digital.")


    # QR Code com infos (imovel|plus|hash)
    qr_payload = f"{info_pluscode.cod_imovel}|{info_pluscode.pluscode_cod}|{info_pluscode.id}"
    qr = qrcode.make(qr_payload)
    qr_buffer = BytesIO()
    qr.save(qr_buffer, format="PNG")
    # qr_buffer.seek(0)
    img = ImageReader(qr_buffer)

    # Mostrar QR code
    c.drawImage(img, width - 180, margin + 40, width=120, height=120)

    # Rodapé 
    c.setStrokeColorRGB(0.5, 0.5, 0.5)
    c.line(margin, margin + 20, width - margin, margin + 20)
    c.setFont("Helvetica-Oblique", 9)
    c.drawCentredString(width/2, margin + 8, "Emitido automaticamente pelo sistema GeoMaps")

    # Moldura do doc
    c.setStrokeColorRGB(0, 0, 0.5)  # azul escuro
    c.setLineWidth(4)
    c.rect(margin, margin, width - 2*margin, height - 2*margin, stroke=1, fill=0)

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer.read(), info_pluscode.id