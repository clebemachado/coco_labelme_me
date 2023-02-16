import cv2
import numpy as np
from skimage.transform import rotate
from skimage.util import random_noise
from skimage import exposure


def imgShow(img: np.ndarray):
    """
    Usada para mostrar uma imagem na tela.
    Arguments:
        img: an np.ndarray
    Returns:
        void
    """
    cv2.imshow("Image", img)
    cv2.waitKey()


def brilho_imagem(image: np.ndarray) -> np.ndarray:
    brilho = np.ones(image.shape, dtype="uint8") * 80
    return cv2.add(image, brilho)


def blur_img(image: np.ndarray) -> np.ndarray:
    return cv2.blur(image,(5,5))


def gama(image: np.ndarray) -> np.ndarray:
    return exposure.adjust_gamma(image, 2)


def noise(image: np.ndarray) -> np.ndarray:
    img = random_noise(image, mode='gaussian')
    return cv2.convertScaleAbs(img, alpha=(255.0))


def flip_image(image: np.ndarray) -> np.ndarray:
    return np.fliplr(image)


def rotate_image(image:np.ndarray, *args):
    """
    Rotaciona uma imagem.
    Arguments:
        image: an np.ndarray
        raio: an int, default is 90
    Return
        np.ndarray
    """
    img = rotate(image, *args, resize=True)
    return cv2.convertScaleAbs(img, alpha=(255.0))

def getTransformacoes() -> dict[str, any]:
    return  {
        'brilho': {
            "function": brilho_imagem,
            "qtd": 0,
            "nome": "brilho",
            "alterable": False
        },
        'blur_img': {
            "function": blur_img,
            "qtd": 0,
            "nome": "blur_img",
            "alterable": False
        },
        'gama': {
            "function": gama,
            "qtd": 0,
            "nome": "gama",
            "alterable": False
        },
        'noise': {
            "function": noise,
            "qtd": 0,
            "nome": "noise",
            "alterable": False
        },
        'flip_image': {
            "function": flip_image,
            "qtd": 0,
            "nome": "flip_image",
            "alterable": True
        },
        'rotate_image': {
            "function": rotate_image,
            "qtd": 0,
            "nome": "rotate_image",
            "alterable": True
        }
    }