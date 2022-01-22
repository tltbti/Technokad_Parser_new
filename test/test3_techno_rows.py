import os
import csv


class TechnokadParser:
    COORD_TYPE = {
        1: "Землепользование",
        2: "Многоконтурный земельный участок",
        3: "Добавление внутреннего контура смежного ЗУ",
        4: "Добавление нескольких внутр контуров смежного ЗУ",
        5: "Землепользование с внутр контуром",
        6: "Линии и окружности",
        7: "Многоконтурный с внутренним контуром",
        8: "При кадастровой ошибке",
        9: "Разветвленный контур",
        10: "Удаление контура МЗУ",
        11: "Уточнение контура МЗУ с удалением контуров и образованием новых",
        12: "Уточнение фрагмента",
    }
    COORD_FORMULA = {
        0: "",
        1: "Mt = √(m₀² + m₁²)",
        2: "Mt = √  ∆ Σ ∫ ± ργ ¼ ½ ¾ ¹²³ ⁿ ᶜ ᵢ ᵦ ₀ ₁ ₂ ₃ ₄ ₅ ₊ ₋ ₌",
        3: "Mt = (mᵦ/ρsinγ)√(d₁²+d₂²)",
        4: "Mt = (mᵦ/ρsin(γ+δ))√((d₁d₂/a)²+(d₂d₃/b)²)",
        5: "Mt = √(m_н² + m_п² + m_к²)",
        6: "Mt = √(m_т² + m_пр²)",
        7: "Mt = √(m_d²+mᵦ²d²/ρ²)",
        8: "Mt = √(m_s²+m_g²)",
        9: "Mt=0.1",
    }
    COORD_METHOD = {
        0: {"": ""},
        1: {692001000000: "Геодезический метод"},
        2: {692002000000: "Фотограмметрический метод"},
        3: {692003000000: "Картометрический метод"},
        4: {692004000000: "Иное описание"},
        5: {692005000000: "Метод спутниковых геодезических измерений Аналитический метод"},
        6: {692006000000: "Аналитический метод"}
    }
    COORD_FILE_EXTENSION_AND_FIRST_ROW = {
        1: {"_1_Земля.csv": ("Контур", "Префикс номера", "Номер", "Старый X", "Старый Y", "Новый X", "Новый Y",
                             "Метод определения",
                             "Формула", "Радиус", "Погрешность", "Описание закрепления")},
        2: {"_2_МЗУ.csv": ("Контур", "Префикс номера", "Номер", "Старый X", "Старый Y", "Новый X", "Новый Y",
                           "Метод определения", "Формула", "Радиус", "Погрешность", "Описание закрепления")},
        3: {"_3_Д_в_к_с_ЗУ.csv": ("Контур", "Префикс номера", "Номер", "Старый X", "Старый Y", "Новый X", "Новый Y",
                                  "Погрешность", "Описание закрепления", "Примечание")},
        4: {"_4_Д_н_в_к_с_ЗУ.csv": ("Контур", "Префикс номера", "Номер", "Старый X", "Старый Y", "Новый X", "Новый Y",
                                    "Погрешность", "Описание закрепления", "Примечание")},
        5: {"_5_З_с_в_к.csv": ("Контур", "Префикс номера", "Номер", "Старый X", "Старый Y", "Новый X", "Новый Y",
                               "Погрешность", "Описание закрепления", "Примечание")},
        6: {"_6_Л_и_о.csv": ("Контур", "Префикс номера", "Номер", "Старый X", "Старый Y", "Новый X", "Новый Y",
                             "Метод определения", "Формула", "Радиус", "Погрешность", "Описание закрепления")},
        7: {"_7_М_с_в_к.csv": ("Контур", "Префикс номера", "Номер", "Старый X", "Старый Y", "Новый X", "Новый Y",
                               "Метод определения", "Формула", "Радиус", "Погрешность", "Описание закрепления")},
        8: {"_8_П_к_о.csv": ("Контур", "Префикс номера", "Номер", "Старый X", "Старый Y", "Новый X", "Новый Y",
                             "Погрешность", "Описание закрепления", "Примечание")},
        9: {"_9_Р_к.csv": ("Контур", "Префикс номера", "Номер", "Старый X", "Старый Y", "Новый X", "Новый Y",
                           "Метод определения", "Формула", "Радиус", "Погрешность", "Описание закрепления")},
        10: {"_10_У_к_МЗУ.csv": ("Контур", "Префикс номера", "Номер", "Старый X", "Старый Y", "Новый X", "Новый Y",
                                 "Метод определения", "Формула", "Радиус", "Погрешность", "Описание закрепления")},
        11: {"_11_У_к_МЗУ_с_у_к_и_о_н.csv": ("Контур", "Префикс номера", "Номер", "Старый X", "Старый Y", "Новый X",
                                             "Новый Y", "Метод определения", "Формула", "Радиус", "Погрешность",
                                             "Описание закрепления")},
        12: {"_12_У_ф.csv": ("Контур", "Префикс номера", "Номер", "Старый X", "Старый Y", "Новый X", "Новый Y",
                             "Погрешность", "Описание закрепления", "Примечание")},
    }

    def __init__(self,
                 path_to_file: str,
                 coord_type: int = 1,
                 coord_formula: int = 0,
                 coord_method: int = 0,
                 inaccuracy: float = 0.10):
        self.path_to_file = path_to_file
        self.coord_type = coord_type
        self.coord_formula = self.COORD_FORMULA.get(coord_formula)
        self.coord_method_number = tuple(self.COORD_METHOD.get(coord_method).keys())[0]
        self.inaccuracy = inaccuracy
        self._new_first_row = tuple(self.COORD_FILE_EXTENSION_AND_FIRST_ROW.get(self.coord_type).values())[0]
        self._raw_data = self._read_from_file_to_list(self.path_to_file)
        self._new_filename = self._get_fullpath_plus_new_name_for_file(self.path_to_file)
        self._new_data = self._convert_data(self._raw_data, self.coord_type, self.coord_formula, self.coord_method_number, self.inaccuracy)
        self._write_file = self._write_csv(self._new_filename,self._new_data)

    def _get_fullpath_plus_new_name_for_file(self, path_to_file: str) -> str:
        """
        :param path_to_file: path to file
        :return: full path to file plus new name for file in string
        """
        old_file_name = os.path.basename(path_to_file)
        old_file_name_without_extension = old_file_name.split(".")[0]
        new_name_ext = tuple(self.COORD_FILE_EXTENSION_AND_FIRST_ROW.get(self.coord_type).keys())[0]
        new_name = old_file_name_without_extension + new_name_ext
        parent_dir = os.path.dirname(path_to_file)
        return os.path.join(parent_dir, new_name)

    def _read_from_file_to_list(self, path_to_file: str, skip_first_row: bool = False) -> [object]:
        """
        Read data from text file with coordinates and return list with rows
        :param path_to_file: path to the file
        :param skip_first_row: skip or not the first row. By default, will be skipped the first row.
        :return: list(CoordRow, CoordRow, ...)
        """

        return_data = []
        with open(path_to_file, "r", encoding="utf-8") as f:
            for enum, i in enumerate(f, 1):
                if skip_first_row:
                    if enum == 1:  # skip the first row
                        continue
                    else:
                        delete_n = str(i).rstrip()  # delete \n
                        split_by_semicolon = delete_n.split(";")
                        return_data.append(self.MyCoordRow(*split_by_semicolon))
                else:
                    delete_n = str(i).rstrip()
                    split_by_semicolon = delete_n.split(";")
                    return_data.append(self.MyCoordRow(*split_by_semicolon))

        return return_data

    def _convert_data(self, data_list: [object], coord_type: int, coord_formula: str, coord_method: int,
                      inaccuracy: float) -> [list]:
        """
        for prepare data to write in file
        :return: list
        """
        # Пробелы потом конвертируются в ";", через библиотеку csv, в функции write_csv (параметр delimeter).
        blank_row = ['' for _ in self._new_first_row]
        blank_row = ['' for _ in self._new_first_row]
        techno_data = []
        if coord_type == 1:
            techno_data = [
                self.TechnokadTypeOfCoordinate.Type_1(
                    contour=row.contour,
                    prefix_number='н',
                    number=row.name,
                    new_x=row.coord_x,
                    new_y=row.coord_y,
                    inaccuracy=str(inaccuracy),
                    formula=coord_formula,
                    method=str(coord_method)
                )
                for row in data_list
            ]

        # вставляем разрывы между контурами
        current_contour = None
        for count, td in enumerate(techno_data):
            if td.contour != current_contour:
                techno_data.insert(count, blank_row)
                current_contour = td.contour

        # десериализуем TechnoRow в строку
        new_techno_data = []
        for count, td in enumerate(techno_data):
            if not isinstance(td, self.TechnokadTypeOfCoordinate.Type_1):
                new_techno_data.append(td)
            else:
                i = td.attr_values_to_list
                new_techno_data.append(i)

        return_data = []
        return_data.append(self._new_first_row)
        return_data = return_data + new_techno_data
        return return_data
    def _write_csv(self,filename, data_list: list):
        with open(filename, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerows(data_list)
            # эта хтонь была взята с благословленного стаковерфло
            # writerow по умолчанию добавляет пустую строку в конец файла
            # и чтобы избваиться от этого пришлось использовать данный хак
            f.seek(0, os.SEEK_END)
            f.seek(f.tell() - 2, os.SEEK_SET)
            f.truncate()

    class MyCoordRow:
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

    class TechnokadTypeOfCoordinate:
        class Type_1:
            """
            для строки Технокада
            Землепользование
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
                return f"{self.__class__.__name__}({', '.join([str(_) for _ in self.__dict__.values()])})"

            @property
            def attr_values_to_list(self):
                return [value for value in self.__dict__.values()]

        class Type_2:
            """
            для строки Технокада
            Многоконтурный земельный участок
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
                return f"{self.__class__.__name__}({', '.join([str(_) for _ in self.__dict__.values()])})"

            @property
            def attr_values_to_list(self):
                return [value for value in self.__dict__.values()]

        class Type_3:
            """
               Класс для строки Технокада-Добавление внутреннего контура смежного ЗУ.
               В соответствии с ней будет создаваться csv файл
            """

            def __init__(self,
                         contour: str = "",
                         prefix_number: str = "",
                         number: str = "",
                         old_x: str = "",
                         old_y: str = "",
                         new_x: str = "",
                         new_y: str = "",
                         inaccuracy: str = "",
                         description: str = "",
                         comment: str = ""):
                self.contour = contour
                self.prefix_number = prefix_number
                self.number = number
                self.old_x = old_x
                self.old_y = old_y
                self.new_x = new_x
                self.new_y = new_y
                self.inaccuracy = inaccuracy
                self.description = description
                self.comment = comment

            def __repr__(self):
                return f"{self.__class__.__name__}({', '.join([str(_) for _ in self.__dict__.values()])})"

            @property
            def attr_values_to_list(self):
                return [value for value in self.__dict__.values()]

        class Type_4:
            """
            для строки Технокада
            Добавление нескольких внутр контуров смежного ЗУ
            """

            def __init__(self,
                         contour: str = "",
                         prefix_number: str = "",
                         number: str = "",
                         old_x: str = "",
                         old_y: str = "",
                         new_x: str = "",
                         new_y: str = "",
                         inaccuracy: str = "",
                         description: str = "",
                         comment: str = ""):
                self.contour = contour
                self.prefix_number = prefix_number
                self.number = number
                self.old_x = old_x
                self.old_y = old_y
                self.new_x = new_x
                self.new_y = new_y
                self.inaccuracy = inaccuracy
                self.description = description
                self.comment = comment

            def __repr__(self):
                return f"{self.__class__.__name__}({', '.join([str(_) for _ in self.__dict__.values()])})"

            @property
            def attr_values_to_list(self):
                return [value for value in self.__dict__.values()]

        class Type_5:
            """
            для строки Технокада
            Землепользование с внутр контуром
            """

            def __init__(self,
                         contour: str = "",
                         prefix_number: str = "",
                         number: str = "",
                         old_x: str = "",
                         old_y: str = "",
                         new_x: str = "",
                         new_y: str = "",
                         inaccuracy: str = "",
                         description: str = "",
                         comment: str = ""):
                self.contour = contour
                self.prefix_number = prefix_number
                self.number = number
                self.old_x = old_x
                self.old_y = old_y
                self.new_x = new_x
                self.new_y = new_y
                self.inaccuracy = inaccuracy
                self.description = description
                self.comment = comment

            def __repr__(self):
                return f"{self.__class__.__name__}({', '.join([str(_) for _ in self.__dict__.values()])})"

            @property
            def attr_values_to_list(self):
                return [value for value in self.__dict__.values()]

        class Type_6:
            """
            для строки Технокада
            Линии и окружности
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
                return f"{self.__class__.__name__}({', '.join([str(_) for _ in self.__dict__.values()])})"

            @property
            def attr_values_to_list(self):
                return [value for value in self.__dict__.values()]

        class Type_7:
            """
            для строки Технокада
            Многоконтурный с внутренним контуром
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
                return f"{self.__class__.__name__}({', '.join([str(_) for _ in self.__dict__.values()])})"

            @property
            def attr_values_to_list(self):
                return [value for value in self.__dict__.values()]

        class Type_8:
            """
            для строки Технокада
            При кадастровой ошибке
            """

            def __init__(self,
                         contour: str = "",
                         prefix_number: str = "",
                         number: str = "",
                         old_x: str = "",
                         old_y: str = "",
                         new_x: str = "",
                         new_y: str = "",
                         inaccuracy: str = "",
                         description: str = "",
                         comment: str = ""):
                self.contour = contour
                self.prefix_number = prefix_number
                self.number = number
                self.old_x = old_x
                self.old_y = old_y
                self.new_x = new_x
                self.new_y = new_y
                self.inaccuracy = inaccuracy
                self.description = description
                self.comment = comment

            def __repr__(self):
                return f"{self.__class__.__name__}({', '.join([str(_) for _ in self.__dict__.values()])})"

            @property
            def attr_values_to_list(self):
                return [value for value in self.__dict__.values()]

        class Type_9:
            """
            для строки Технокада
            Разветвленный контур
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
                return f"{self.__class__.__name__}({', '.join([str(_) for _ in self.__dict__.values()])})"

            @property
            def attr_values_to_list(self):
                return [value for value in self.__dict__.values()]

        class Type_10:
            """
            для строки Технокада
            Удаление контура МЗУ
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
                return f"{self.__class__.__name__}({', '.join([str(_) for _ in self.__dict__.values()])})"

            @property
            def attr_values_to_list(self):
                return [value for value in self.__dict__.values()]

        class Type_11:
            """
            для строки Технокада
            Удаление контура МЗУ
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
                return f"{self.__class__.__name__}({', '.join([str(_) for _ in self.__dict__.values()])})"

            @property
            def attr_values_to_list(self):
                return [value for value in self.__dict__.values()]

        class Type_12:
            """
            для строки Технокада
            Удаление контура МЗУ
            """

            def __init__(self,
                         contour: str = "",
                         prefix_number: str = "",
                         number: str = "",
                         old_x: str = "",
                         old_y: str = "",
                         new_x: str = "",
                         new_y: str = "",
                         inaccuracy: str = "",
                         description: str = ""):
                self.contour = contour
                self.prefix_number = prefix_number
                self.number = number
                self.old_x = old_x
                self.old_y = old_y
                self.new_x = new_x
                self.new_y = new_y
                self.inaccuracy = inaccuracy
                self.description = description

            def __repr__(self):
                return f"{self.__class__.__name__}({', '.join([str(_) for _ in self.__dict__.values()])})"

            @property
            def attr_values_to_list(self):
                return [value for value in self.__dict__.values()]


filepath =r"M:\Материалы_Заказчиков\НПО Лавочкина Химки\геодезия\готовая\корпус_!!.txt"
TechnokadParser(filepath)