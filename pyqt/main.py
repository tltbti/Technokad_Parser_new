import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout

app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
# btns = (QPushButton('Top'), QPushButton('Bottom'))
layout.addWidget(QPushButton('Top'))
layout.addWidget(QPushButton('Bottom'))
window.setLayout(layout)
window.show()
app.exec()