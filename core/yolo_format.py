import glob2
import json
from utils import TypeShape
import itertools
import os
import shutil

# Exemplo path
"""
imgs/
    img_1.png
    img_1.json
    img_2.png
    img_2.json
"""

def read_json_to_dict(path:str):
    dict_data = []
    for path_json in glob2.glob(path + "\\*.json"):
        with open(path_json) as file:
            dict_data.append(json.load(file))

    return dict_data

def criar_diretorio(path:str):
    if not os.path.exists(path):
        os.mkdir(path)
        print(f"Path criado: {path}")
    else:
        shutil.rmtree(path)
        os.mkdir(path)
        print(f"Path criado: {path}")

def convert_instance(path:str, type_shape:TypeShape):
    img_files = read_json_to_dict(path)
    print("Qtd para ser convertida: ", len(img_files))

    destino_path = path + "\\data_coco"
    criar_diretorio(destino_path)

    for data in img_files:
        h, w, name = [data[x] for x in ["imageHeight", "imageWidth", "imagePath"]]

        labels_destino = destino_path + "\\" + name.split(".")[0] + ".txt"

        shapes = data["shapes"]
        shapes = [d_r for d_r in shapes if d_r["shape_type"] == type_shape.value]

        if(len(shapes) == 0):
            continue

        for dict_shape in shapes:
            list_points = list(itertools.chain(*dict_shape["points"]))
            points = [0] + [j / w if i % 2 == 0 else j / h for i, j in enumerate(list_points)]
            text = ' '.join(str(x) for x in points)
            with open(labels_destino, "a") as f:
                f.write(text + "\n")
                f.close()

        # Copy IMG
        shutil.copyfile(path + "\\"  + name, destino_path + "\\" + name)
