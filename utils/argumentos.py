import argparse

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-r",'--rename', action='store_true', help = "Função para renomear as imagens.")
group.add_argument("-da",'--data_argumentation', action='store_true', help = "Função para criar novas imagens.")
group.add_argument("-yf",'--yolo_format', action='store_true', help = "Função para gerar o formato yolo.")
parser.add_argument("-p","--path", help="Origem das imagens", required=True, type=str)
parser.add_argument("-t", "--type_shape", help="Forma da marcação: Polígono[p], Retangulo[r]", choices=["p", "r"])
args = parser.parse_args()