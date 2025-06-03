import os
import shutil

pasta = 'browser/screenshot'

for item in os.listdir(pasta):
    caminho = os.path.join(pasta, item)
    if os.path.isfile(caminho) or os.path.islink(caminho):
        os.unlink(caminho)  # Remove arquivo ou link simbólico
    elif os.path.isdir(caminho):
        shutil.rmtree(caminho)  # Remove diretório e todo o conteúdo
