import os
import csv


class TechnokadParser:
    def __init__(self, path_to_file: str, extension: str = '_zemlya.csv'):
        self.path_to_file = path_to_file
        self.extension = extension
        self._raw_data = self._read_from_file_to_list(path_to_file)
        self._new_name = self._get_add_extension_to_file_name(path_to_file, self.extension)
        self._new_data = self._prepare_data(self._raw_data)
        self._write_data = self._write_csv(self._new_data)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.path_to_file},{self.extension})"

    def _get_add_extension_to_file_name(self, path_to_file: str, new_name_with_extension: str) -> str:
        """
        :param path_to_file: path to file
        :param new_name_with_extension: file mask with extension will be added to end of filename
        :return: full path to file in string
        example new_file_name("D:\!Python_test\!Ready\Parser for technokad\coord.txt", "_2.csv")\n
        -> "D:\!Python_test\!Ready\Parser for technokad\coord_2.csv"
        """
        old_file_name = os.path.basename(path_to_file)
        old_file_name_without_extension = old_file_name.split(".")[0]
        new_name = old_file_name_without_extension + new_name_with_extension
        parent_dir = os.path.dirname(path_to_file)
        return os.path.join(parent_dir, new_name)

    def _read_from_file_to_list(self, path_to_file, skip_first_row: bool = False) -> [object]:
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
                        delete_n = str(i).rstrip()  # delete \n
                        split_by = delete_n.split(";")
                        row_list.append(self.OurRow(*split_by))
                else:
                    delete_n = str(i).rstrip()
                    split_by = delete_n.split(";")
                    row_list.append(self.OurRow(*split_by))

        return row_list

    def _prepare_data(self, data_list: [object]) -> [list]:
        """
        for prepare data to write in file
        :return: list
        """
        self.data_list = self._raw_data
        FIRST_ROW_TECHNOKAD = ["Контур", "Префикс номера", "Номер", "Старый X", "Старый Y", "Новый X", "Новый Y",
                               "Метод определения",
                               "Формула", "Радиус", "Погрешность", "Описание закрепления"]
        # Пробелы потом конвертируются в ";", через библиотеку csv, в функции write_csv (параметр delimeter).
        BLANK_ROW = ['' for _ in FIRST_ROW_TECHNOKAD]

        techno_data = [
            self.TechnokadRowZemlepolizovanie(contour=row.contour,
                                              prefix_number="н",
                                              number=row.name,
                                              new_x=row.coord_x,
                                              new_y=row.coord_y,
                                              inaccuracy="0,1",
                                              description="626003000000")
            for row in data_list]

        # вставляем разрывы между контурами
        current_contour = None
        for count, td in enumerate(techno_data):
            if td.contour != current_contour:
                techno_data.insert(count, BLANK_ROW)
                current_contour = td.contour

        # десериализуем TechnoRow в строку
        new_techno_data = []
        for count, td in enumerate(techno_data):
            if not isinstance(td, self.TechnokadRowZemlepolizovanie):
                new_techno_data.append(td)
            else:
                i = td.attr_values_to_list
                new_techno_data.append(i)

        return_data = []
        return_data.append(FIRST_ROW_TECHNOKAD)
        return_data = return_data + new_techno_data
        return return_data

    def _write_csv(self, data_list: list):
        with open(self._new_name, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerows(data_list)
            # эта хтонь была взята с благословленного стаковерфло
            # writerow по умолчанию добавляет пустую строку в конец файла
            # и чтобы избваиться от этого пришлось использовать данный хак
            f.seek(0, os.SEEK_END)
            f.seek(f.tell() - 2, os.SEEK_SET)
            f.truncate()

    class TechnokadRowZemlepolizovanie:
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
            return f"{self.__class__.__name__}({self.contour},{self.prefix_number},{self.number},{self.old_x},{self.old_y},{self.new_x},{self.new_y},{self.method},{self.formula},{self.radius},{self.inaccuracy},{self.description})"

        @property
        def attr_values_to_list(self):
            return [value for value in self.__dict__.values()]

    class OurRow:
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
            self.contour = f"{contour.split('/')[0]}"
            self.type = type

        def __repr__(self):
            return f"{self.__class__.__name__}('{self.number}','{self.name}','{self.coord_x}','{self.coord_y}','{self.contour}','{self.type}')"

        def __str__(self):
            return f"{self.number};{self.name};{self.coord_x};{self.coord_y};{self.contour};{self.type}"

        @property
        def get_semicolon_string(self) -> str:
            return ";".join(['' for value in self.__dict__.values()])

        @property
        def get_blank_str(self) -> list:
            return ['' for value in self.__dict__.values()]


file = r"M:\Материалы_Заказчиков\НПО Лавочкина Химки\геодезия\готовая\корпус_!!.txt"

TechnokadParser(file)
