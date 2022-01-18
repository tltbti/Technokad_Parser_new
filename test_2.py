import csv

file = r"D:\!Python_test\!Ready\Parser for technokad\coord.txt"


class TechnokadRow:
    """
    Класс для строки Технокада, в соответствии с ней будет создаваться csv файл
    """

    def __init__(self,
                 contour: str = "",
                 prefix_number: str = "",
                 number: str = "",
                 old_x: str = "",
                 old_y: str = "",
                 new_x: str = "",
                 new_y: str = "",
                 method: str = "",
                 formula: str = "",
                 radius: str = "",
                 inaccuracy: str = "",
                 description: str = ""):
        self.contour = contour
        self.prefix_number = prefix_number
        self.number = number
        self.old_x = old_x
        self.old_y = old_y
        self.new_x = new_x
        self.new_y = new_y
        self.method = method
        self.formula = formula
        self.radius = radius
        self.inaccuracy = inaccuracy
        self.description = description

    def __repr__(self):
        return f"TechnoRow({self.contour},{self.prefix_number},{self.number},{self.old_x},{self.old_y},{self.new_x},{self.new_y},{self.method},{self.formula},{self.radius},{self.inaccuracy},{self.description})"

    @property
    def attr_values_to_list(self):
        return [value for value in self.__dict__.values()]


class MyRow:
    """
    класс строки из МЕНЮГЕО от геодезистов, в таком виде они выгружают координаты
    :param self.number: номер координаты
    :param name: имя координаты
    :param coord_x: координата х
    :param coord_y: координата у
    :param contour: номер контура
    :param type: тип контура (подземный, надземный)
    """

    def __init__(self, number: str, name: str, coord_x: str, coord_y: str, contour: str, type: str):
        self.number = number
        self.name = name
        self.coord_x = str(round(float(coord_x), 2))
        self.coord_y = str(round(float(coord_y), 2))
        self.contour = f"[{contour.split('/')[0]}]"
        self.type = type

    def __repr__(self):
        return f"CoordRow('{self.number}','{self.name}','{self.coord_x}','{self.coord_y}','{self.contour}','{self.type}')"

    def __str__(self):
        return f"{self.number};{self.name};{self.coord_x};{self.coord_y};{self.contour};{self.type}"

    @property
    def get_blank_str(self) -> list():
        return ['' for value in self.__dict__.values()]


def read_from_file_to_list(path_to_file: str = file, skip_first_row: bool = True) -> [object]:
    """
    Read data from text file with coordinates and return list with rows
    :param path_to_file: path to the file
    :param skip_first_row: skip or not the first row. By default, will be skipped the first row.
    :return: list(CoordRow, CoordRow, ...)
    """

    row_list = []
    with open(path_to_file, "r", encoding="utf-8") as f:
        for enum, i in enumerate(f, 1):
            if skip_first_row:
                if enum == 1:  # skip the first row
                    continue
                else:
                    delete_n = str(i).rstrip()  # delete /n
                    split_by = delete_n.split(";")
                    row_list.append(MyRow(*split_by))
            else:
                delete_n = str(i).rstrip()
                split_by = delete_n.split(";")
                row_list.append(MyRow(*split_by))

    return row_list


def insert_blank_list(data_list: [object]) -> list:
    blank_list = data_list[0].get_blank_str
    current_contour = data_list[0].contour
    for enum, row in enumerate(data_list):
        if current_contour != row.contour:
            data_list.insert(enum, blank_list)
            current_contour = row.contour
    return data_list

r = read_from_file_to_list()
row_data = insert_blank_list(r)
print(row_data)

def write_csv():
    with open("CSV_2.csv", "w", encoding="utf-8", newline="") as f:
        FIRST_ROW_TECHNOKAD = ["Контур", "Префикс", "номера", "Номер", "Старый X", "Старый Y", "Новый X", "Новый Y",
                               "Метод определения",
                               "Формула", "Радиус", "Погрешность", "Описание закрепления"]
        SECOND_ROW_TECHNOKAD = ['' for i in FIRST_ROW_TECHNOKAD]
        data = [FIRST_ROW_TECHNOKAD, SECOND_ROW_TECHNOKAD]
        techno_data = [TechnokadRow(contour=row.contour, prefix_number="н", number=row.number, new_x=row.coord_x,
                                    new_y=row.coord_y, inaccuracy="0,1", description="626003000000").attr_values_to_list for
                       row in
                       row_data]
        writer = csv.writer(f, delimiter=';')
        writer.writerows(data)
