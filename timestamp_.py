from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os

def adicionar_timestamp(imagem_path, tamanho_fonte=30):
    if not os.path.exists(imagem_path):
        raise FileNotFoundError(f"Imagem não encontrada: {imagem_path}")

    imagem = Image.open(imagem_path).convert("RGB")
    draw = ImageDraw.Draw(imagem)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        fonte_path = "arial.ttf"  # fonte de sistema para informar o valor do timestamp
        fonte = ImageFont.truetype(fonte_path, tamanho_fonte)
    except:
        fonte = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), timestamp, font=fonte)
    largura_texto = bbox[2] - bbox[0]
    altura_texto = bbox[3] - bbox[1]

    margem = 30
    padding = 20

    largura_imagem, altura_imagem = imagem.size
    x = largura_imagem - largura_texto - margem
    y = altura_imagem - altura_texto - margem

    # Retângulo preto atrás do texto
    draw.rectangle(
        [(x - padding, y - padding), (x + largura_texto + padding, y + altura_texto + padding)],
        fill="black"
    )

    # Texto branco por cima
    draw.text((x, y), timestamp, font=fonte, fill="white")

    imagem.save(imagem_path)
    return imagem_path
