import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QCoreApplication
import design  # Это наш конвертированный файл дизайна


# функция для обработки строки, находит номер контура и преобразовывает его в соответствии с требованиями Технокада
def change_string(my_str):
    if my_str.find(',') > 0:
        edit_my_str = my_str.split(',')
    else:
        edit_my_str = my_str.split(';')
    temp_list = []
    for index, item in enumerate(edit_my_str):
        if index == 4:
            clear_symbol = item.split('/').pop(0)
            temp_list.append(f'[{clear_symbol}]')
        else:
            temp_list.append(item)
    return ';'.join(temp_list)


# функция для переименовывания файла
def rename_file(file, mask='_исправленный'):
    splitter = file.split('.')
    return splitter[0] + mask + '.' + splitter[1]


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        # Кнопка ВЫХОД
        # self.pushButton.clicked.connect(QCoreApplication.instance().quit)
        # self.pushButton_2.clicked.connect(connection.close())
        # connection.close()
        # Строка ВВОДА
        # self.lineEdit.text()
        self.lineEdit
        # Кнопка ОК
        self.pushButton.clicked.connect(self.onButtonClicked)

    def onButtonClicked(self):
        def writer(file):
            file = file.replace('"', '')
            file_read = open(file)
            file_write = open(rename_file(file), 'w')
            counter = 0
            counter_main = 0
            for line in file_read:
                counter_main += 1
                if counter_main > 1:
                    change_string(line)
                    start = change_string(line).find('[')
                    end = change_string(line).find(']')
                    symbol = ''
                    if counter >= 1:
                        key_value2 = change_string(line)[start + 1:end]
                        if key_value != key_value2:
                            key_value = change_string(line)[start + 1:end]
                            symbol = '\n'
                    key_value = change_string(line)[start + 1:end]
                    counter += 1
                    file_write.write(symbol + change_string(line))
            file_write.close()
            file_read.close()

        writer(self.lineEdit.text())


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    app.setStyle('Fusion')  # задаем стиль окон
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
