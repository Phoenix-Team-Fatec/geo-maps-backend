from PIL import Image
from io import BytesIO
import base64
from bson import Binary


def compress_image(contents):
    # Buffer que irá armazenar a imagem comprimida
    buffer = BytesIO()

    image = Image.open(BytesIO(contents))

    # Comprimindo
    image.save(buffer, format='WEBP', quality=60, optimize=True)
    compressed_bytes = buffer.getvalue()
    
    size_bytes = buffer.tell() 
    
    size_mb = size_bytes / (1024 ** 2)
    
    if size_mb > 5:
        raise Exception("Tamanho do arquivo maior que 5 mb")
    
    return compressed_bytes
    
def process_property_photo(properties:dict) -> dict:
    """
    Função para converter Binary da foto para base64 string
    """  
    # Verifica se o objeto 'photo' está no objeto
    if 'photo' in properties:
        photo_data = properties['photo']
        
        # Verifica se a 'photo' é um dicionário
        if isinstance(photo_data, dict):
            image_binary = photo_data.get('image_data')
            
            # Realiza a conversão de Binary para base64 string
            if isinstance(image_binary, (Binary, bytes)):
                binary_bytes = bytes(image_binary)
                base64_str = base64.b64encode(binary_bytes).decode('utf-8')
                properties['photo'] = base64_str     
    
    return properties
