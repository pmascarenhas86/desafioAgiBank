from PIL import Image
import os


def reduzir_imagens_em_pasta(caminho_pasta, proporcao=0.75):
    for arquivo in os.listdir(caminho_pasta):
        if arquivo.lower().endswith(".png"):
            caminho_imagem = os.path.join(caminho_pasta, arquivo)

            with Image.open(caminho_imagem) as img:
                nova_largura = int(img.width * proporcao)
                nova_altura = int(img.height * proporcao)
                imagem_redimensionada = img.resize((nova_largura, nova_altura), Image.LANCZOS)
                imagem_redimensionada.save(caminho_imagem)

                print(f"Redimensionada: {caminho_imagem}")

# Exemplo de uso

reduzir_imagens_em_pasta("browser\screenshot")