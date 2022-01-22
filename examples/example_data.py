COORD_TYPE = {
    1: {"Землепользование": "_1_Земля.csv"},
    2: {"Многоконтурный земельный участок": "_2_МЗУ.csv"},
    3: {"Добавление внутреннего контура смежного ЗУ": "_3_Д_в_к_с_ЗУ.csv"},
    4: {"Добавление нескольких внутр контуров смежного ЗУ": "_4_Д_н_в_к_с_ЗУ.csv"},
    5: {"Землепользование с внутр контуром": "_5_З_с_в_к.csv"},
    6: {"Линии и окружности": "_6_Л_и_о.csv"},
    7: {"Многоконтурный с внутренним контуром": "_7_М_с_в_к.csv"},
    8: {"При кадастровой ошибке": "_8_П_к_о.csv"},
    9: {"Разветвленный контур": "_9_Р_к.csv"},
    10: {"Удаление контура МЗУ": "_10_У_к_МЗУ.csv"},
    11: {"Уточнение контура МЗУ с удалением контуров и образованием новых": "_11_У_к_МЗУ_с_у_к_и_о_н.csv"},
    12: {"Уточнение фрагмента": "_12_У_ф.csv"},
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
    1: {692001000000: "Геодезический метод"},
    2: {692002000000: "Фотограмметрический метод"},
    3: {692003000000: "Картометрический метод"},
    4: {692004000000: "Иное описание"},
    5: {692005000000: "Метод спутниковых геодезических измерений"},
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


class SelectCoordType:
    def __init__(self, selector: int):
        self._selector = selector
        self.first_row = tuple(COORD_FILE_EXTENSION_AND_FIRST_ROW.get(selector).values())[0]
        self.file_ext = tuple(COORD_FILE_EXTENSION_AND_FIRST_ROW.get(selector).keys())[0]



a = 1
b = tuple(item_name.get(a).items())
print(b)
print(b[0][0], type(b[0][0]))
print(b[0][1], type(b[0][1]))