file = r"D:\!Python_test\!Ready\Parser for technokad\coord.txt"

s = '1;1;418192.8660;1322826.4820;1/2;1'


class MyRow:
    """
    :param self.number: номер координаты
    :param name: имя координаты
    :param coord_x: координата х
    :param coord_y: координата у
    :param contour: номер контура
    :param type: тип контура (подземный, надземный)
    """

    def __init__(self, number: str, name: str, coord_x: float, coord_y: float, contour: str, type: str):
        self.number = number
        self.name = name
        self.coord_x = round(float(coord_x), 2)
        self.coord_y = round(float(coord_y), 2)
        self.contour = f"[{contour.split('/')[0]}]"
        self.type = type

    def __repr__(self):
        return f"CoordRow('{self.number}','{self.name}','{self.coord_x}','{self.coord_y}','{self.contour}','{self.type}')"

    def __str__(self):
        return f"{self.number};{self.name};{self.coord_x};{self.coord_y};{self.contour};{self.type}"

    @property
    def row_all(self):
        return f"{self.number};{self.name};{self.coord_x};{self.coord_y};{self.contour};{self.type}\n"


def read_from_file_to_list(path_to_file: str = file, skip: bool = True) -> list:
    """
    Read data from text file with coordinates and return list with rows
    :param path_to_file: path to the file
    :param skip: skip or not the first row. By default, will be skipped the first row.
    :return: list(CoordRow, CoordRow, ...)
    """
    row_list = []
    with open(path_to_file, "r", encoding="utf-8") as f:
        for enum, i in enumerate(f, 1):
            if skip:
                if enum == 1: # skip the first row
                    continue
                else:
                    delete_n = str(i).rstrip() # delete /n
                    split_by = delete_n.split(";")
                    row_list.append(MyRow(*split_by))
            else:
                delete_n = str(i).rstrip()
                split_by = delete_n.split(";")
                row_list.append(MyRow(*split_by))
    return row_list

row_data = read_from_file_to_list(file)

print(row_data)


filename_input = f"AAAA_исправленный2.txt"
with open(filename_input, "w", encoding="utf-8") as file_w:
    row_contour = None
    for row in row_data:
        if row_contour == row.contour:
            file_w.write(row.row_all)
        else:
            file_w.write("\n")
            file_w.write(row.row_all)
        row_contour = row.contour


def create_file(select_type_of_file: int) -> file:
    """
    Примеры csv-файлов взяты из раздела 3.2.17 (https://www.technokad.ru/support/faq/) с сайтса Технокада
    https://www.technokad.ru/upload/www/files/faq/3.2.17.zip

    1 -  Землепользование
    2 -  Многоконтурный земельный участок
    3 -  Добавление внутреннего контура смежного ЗУ
    4 -  Добавление нескольких внутренних контуров смежного ЗУ
    5 -  Землепользование с внутр контуром
    6 -  Линии и окружности
    7 -  Многоконтурный с внутренним контуром
    8 -  При кадастровой ошибке
    9 -  Разветвленный контур
    10 - Удаление контура МЗУ
    11 - Уточнение контура МЗУ с удалением контуров и образованием новых
    12 - Уточнение фрагмента
    :param select_type_of_file:
    :return: call a function and create file
    """
    type_of_files = {
        1: file_1_zemlepolizovanie(),
        2: file_2_mnogokonturnyj_zemelnyj_uchastok(),
        3: file_3_dobavlenie_vnutrennego_kontura_smezhnogo_zu(),
        4: file_4_dobavlenie_neskolkih_vnutrennih_konturov_smezhnogo_zu(),
        5: file_5_zemlepolzovanie_s_vnutrennim_konturom(),
        6: file_6_linii_i_okruzhnosti(),
        7: file_7_mnogokonturnyj_s_vnutrennim_konturom(),
        8: file_8_pri_kadastrovoj_oshibke(),
        9: file_9_razvetvlennyj_kontur(),
        10: file_10_udalenie_kontura_mzu(),
        11: file_11_utochnenie_kontura_mzu_s_udaleniem_konturov_i_obrazovaniem_novyh(),
        12: file_12_utochnenie_fragmenta()
    }
    return type_of_files[select_type_of_file]


def file_1_zemlepolizovanie(filename: str = "тест") -> file:
    """
    Создает файл землепользование
    :return:
    """
    filename = f"{filename}_землепользование"
    with open(filename_input, "w", encoding="utf-8") as f:
        row_contour = None
        first_string = "Контур;Префикс номера;Номер;Старый X;Старый Y;Новый X;Новый Y;Метод определения;Формула;Радиус;Погрешность;Описание закрепления\n"
        second_string = ";;;;;;;;;;;"
        f.write(first_string)
        f.write(second_string)
        for row in row_data:
            if row_contour == row.contour:
                f.write(row.row_all)
            else:
                f.write("\n")
                f.write(row.row_all)
            row_contour = row.contour


def file_2_mnogokonturnyj_zemelnyj_uchastok():
    """
    Создает файл землепользование
    :return:
    """
    pass


def file_3_dobavlenie_vnutrennego_kontura_smezhnogo_zu():
    """
    Создает файл землепользование
    :return:
    """
    pass


def file_4_dobavlenie_neskolkih_vnutrennih_konturov_smezhnogo_zu():
    """
    Создает файл землепользование
    :return:
    """
    pass


def file_5_zemlepolzovanie_s_vnutrennim_konturom():
    """
    Создает файл землепользование
    :return:
    """
    pass


def file_6_linii_i_okruzhnosti():
    """
    Создает файл землепользование
    :return:
    """
    pass


def file_7_mnogokonturnyj_s_vnutrennim_konturom():
    """
    Создает файл землепользование
    :return:
    """
    pass


def file_8_pri_kadastrovoj_oshibke():
    """
    Создает файл землепользование
    :return:
    """
    pass


def file_9_razvetvlennyj_kontur():
    """
    Создает файл землепользование
    :return:
    """
    pass


def file_10_udalenie_kontura_mzu():
    """
    Создает файл землепользование
    :return:
    """
    pass


def file_11_utochnenie_kontura_mzu_s_udaleniem_konturov_i_obrazovaniem_novyh():
    """
    Создает файл землепользование
    :return:
    """
    pass


def file_12_utochnenie_fragmenta():
    """
    Создает файл землепользование
    :return:
    """
    pass
