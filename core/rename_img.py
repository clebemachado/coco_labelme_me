import shutil

import glob2
import os
MSG_CRIADO_PATH = "Path criado com sucesso"

# Exemplo do como o path deve ser
"""
    img_1/
        abc.png
        def.png
    img_2/
        ghi.png
        jlk.png
"""

def rename_img(path_origem:str):
    path_destino = path_origem + "\\rename_img"

    if not os.path.exists(path_destino):
        os.mkdir(path_destino)
        print(f"{MSG_CRIADO_PATH}: {path_destino}")
    else:
        shutil.rmtree(path_destino)
        os.mkdir(path_destino)
        print(f"{MSG_CRIADO_PATH}: {path_destino}")

    for path in os.listdir(path_origem):
        for number, pathImg in enumerate(glob2.glob(f"{path_origem}\\{path}" + "\\*.jpg")):
            FILE_NAME = f"{path}_{number}"
            PATH_TARGET = path_destino + "\\" + FILE_NAME + "." + pathImg.split(".")[-1]
            shutil.copyfile(pathImg, PATH_TARGET)

