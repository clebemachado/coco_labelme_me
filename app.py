from utils import args, TypeShape
from core import rename_img, convert_instance, data_argumentation

if __name__ == "__main__":

    if not(args.rename or args.yolo_format or args.data_argumentation):
        raise("No máximo uma ação é requisitada: [-r: rename, -yf: yolo_format, -da: data_atgumentation]")

    if args.rename:
        rename_img(args.path)

    if args.yolo_format:
        if args.type_shape is None:
            raise("Tipo da forma deve ser especificado: [c, p]")

        type_shape = None
        if args.type_shape == "r":
            type_shape = TypeShape.RECTANGLE
        else:
            type_shape = TypeShape.POLIGON

        convert_instance(args.path, type_shape)

    if args.data_argumentation:
        data_argumentation(args.path)