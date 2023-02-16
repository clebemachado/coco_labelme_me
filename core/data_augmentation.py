import cv2
import math
import numpy as np
import itertools
import random
from utils import getTransformacoes
import os

def process_points(line: str, img: np.ndarray):
    """
    Processa os pontos no formato yolo '0 0.23076923076923078 0.49290060851926976 0.22913256955810146 ... para ex: [[120, 255], [125, 256], ...]
    No array acima, o primeiro valor é a classe (quer será removida), o segundo é na posição X, o terceiro Y, o quarto é X, o quinto Y....
    No fim, será feito pares entre esses valores, ex: [[primeiro_y, primeiro_x], ["segundo_y, segundo_x"], ...]

    Arguments:
        line: as str -> ex: '0 0.23076923076923078 0.49290060851926976'
        img: as np.ndarray
    return
        [[valor_y, valor_x], [valor_y_2, valor_x_2], ...]
    """

    h, w, _ = img.shape
    points = [
        math.floor(float(point) * w) if idx % 2 == 1 else math.floor(float(point) * h)
        for idx, point in enumerate(line.split(" "))
    ]
    points.pop(0)
    pares, impares = points[0::2], points[1::2]
    points = [[pares[i], impares[i]] for i in range(len(pares))]
    return points


def get_points_text(img: np.ndarray, path_point: str) -> list:
    """
    Pega todos os pontos de um arquivo yolo.
    Arguments:
        img: an np.ndarray
        path_point: an str
    Returns:
        list de points
    """
    all_points = []
    with open(path_point) as f:
        for line in f.readlines():
            all_points.append(process_points(line, img))
    return all_points


def fill_poly(all_points: list, img: np.ndarray):
    """
    Retorna uma lista de threshold de acordo com as marcações yolo.
    Arguments:
        all_points: lista de pontos yolo
    Returns:
        list de threshold
    """

    all_imgs = []

    for point in all_points:
        blackFrame = 0 * np.ones(img.shape, np.uint8)
        pts = np.array(point, np.int32)
        pts = pts.reshape((-1, 1, 2))
        all_imgs.append(cv2.fillPoly(blackFrame, [pts], (255, 255, 255)))
        # all_imgs.append(cv2.polylines(blackFrame,[pts],True,(255,255,255)))

    return all_imgs


def fill_poly_points(img:np.ndarray, path:str) -> list:
    """
    Retorna uma lista de threshold.
    Arguments:
        img: np.ndarray
        path: as str
    Returns:
        list de threshold
    """
    all_points = get_points_text(img, path)
    all_imgs = fill_poly(all_points, img)
    return all_imgs


def get_contornos_poly_yolo_format(img: np.ndarray) -> str:
    """
    Pega os contornos do threshold e converte em poligonos.
    Arguments:
        img: np.ndarray
    Returns:
        retorna um str no formato yolo
    """
    image = np.copy(img)
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Procurar arestas
    edged = cv2.Canny(img_gray, 100,
                      200)  # 100 -> Limite Mínimo; 200 -> Limite superior; Geralmente fica 127 gray scale
    contornos, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    contornos = list(itertools.chain.from_iterable(contornos))
    h, w, _ = image.shape
    yolo_format = ["0"] + [f"{i[0][0] / w} {i[0][1] / h}" for i in contornos]
    list_text = " ".join(yolo_format).split(" ")
    return " ".join(list_text)


def salvar_contorno_amostra(lines: list, img: np.ndarray, path_destino: str, name_img:str, number:int):

    """
    Função para salvar uma copia do contorno gerado.
    :param lines: lista de pontos do polígono
    :param img: ndarray que é uma imagem
    :param path_destino: path onde será salvo
    :param name_img: nome da imagem; Deve ser igual o original
    :param number: numero para marcação da imagem
    :return: void
    """

    points = []
    for line in lines:
        points.append(process_points(line, img))

    blackFrame = 0 * np.ones(img.shape, np.uint8)
    for point in points:
        pts = np.array(point, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(blackFrame, [pts], True, (255, 255, 255))

    path_destino = path_destino.replace("processada", "contornos_amostra")

    if not os.path.exists(path_destino):
        os.mkdir(path_destino)

    cv2.imwrite(f"{path_destino}\\{name_img}_{number}.jpg", blackFrame)


def selectFunction(dict_functions):

    """
    Essa função retorna uma função para manipulação de imagem, como noise, flip e outras.
    :param dict_functions: dict[functions]
    :return: function[function], nome[str], alterable[boolean]
    """

    function = None
    nome = None
    alterable = False

    functionIsSelected = False

    keys = list(dict_functions.keys())

    while (not functionIsSelected):
        idx = random.randint(0, len(keys) - 1)
        key = keys[idx]
        if dict_functions[key]["qtd"] != 0:
            continue
        dict_functions[key]["qtd"] = 1
        functionIsSelected = True
        function = dict_functions[key]['function']
        nome = dict_functions[key]['nome']
        alterable = dict_functions[key]["alterable"]

    return function, nome, alterable


def data_argumentation(path_imgs:str):
    """
    # ESTRUTURA
        imgs/
            img_1.png
            img_1.txt
            img_2.png

    Função para criar outras imagens
    :param path_imgs:
    :return:
    """
    list_paths = os.listdir(path_imgs)
    for path in list_paths:

        if (".jpg" not in path):
            continue

        ## GET ALL FUNCTIONS
        dict_functions = getTransformacoes()

        NAME_IMG = path.replace(".jpg", "")
        PATH_FILE = path.replace("jpg", "txt")

        # IF NÃO TIVER O TXT, NÃO CONTINUAR
        if PATH_FILE not in list_paths:
            continue

        PATH_POINT = path_imgs + "\\" + PATH_FILE
        PATH_IMG = path_imgs + "\\" + path
        PATH_DESTINO = path_imgs + "\\processada"

        # TODO -> CRIAR UMA FUNÇÃO PADRÃO PARA ISSO
        if not os.path.exists(PATH_DESTINO):
            os.mkdir(PATH_DESTINO)

        ## Load img PATH
        img = cv2.imread(PATH_IMG)

        qtd_functions = random.randint(4, len(dict_functions))

        for number in range(1, qtd_functions):

            function_image, nome, alterable = selectFunction(dict_functions)

            img_copy = np.copy(img)
            thresholds_list = fill_poly_points(img_copy, PATH_POINT)
            ## load points

            list_poligonos = []

            if nome == "rotate_image":
                raios = [90, 180, 270]
                idx = random.randint(0, len(raios) - 1)
                raio = raios[idx]
                img_copy = function_image(img_copy, raio)
                for imagem in thresholds_list:
                    img_threshold_ = function_image(imagem, raio)
                    yolo_format = get_contornos_poly_yolo_format(img_threshold_)
                    list_poligonos.append(yolo_format)

            elif nome == "flip_image":
                img_copy = function_image(img_copy)
                for imagem in thresholds_list:
                    img_threshold_ = function_image(imagem)
                    yolo_format = get_contornos_poly_yolo_format(img_threshold_)
                    list_poligonos.append(yolo_format)

            else:
                img_copy = function_image(img_copy)
                for imagem in thresholds_list:
                    yolo_format = get_contornos_poly_yolo_format(imagem)
                    list_poligonos.append(yolo_format)

            cv2.imwrite(f"{PATH_DESTINO}\\{NAME_IMG}_{number}.jpg", img_copy)

            for line_ in list_poligonos:
                NAME_FOR_FILE = PATH_FILE.replace(".txt", "")
                with open(f"{PATH_DESTINO}\\{NAME_FOR_FILE}_{number}.txt", "a") as f:
                    f.write(line_ + "\n")
                    f.close()

            salvar_contorno_amostra(list_poligonos, img_copy, PATH_DESTINO, NAME_IMG, number)
