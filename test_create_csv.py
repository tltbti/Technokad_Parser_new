select_item = {
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
    12: "Уточнение фрагмента"
}
print("Выберите вариант файла (введите цифру):")
for number, name in select_item.items():
    print(f"{number}: {name}")

s = int(input("Я выбираю: "))

print(f"Вы выбрали\n"
      f"{s}-{select_item.get(s)}")
