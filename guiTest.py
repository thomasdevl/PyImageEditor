from PySide6.QtWidgets import *
import os
import sys

def on_clicked():
    print("Clicked")

def main():
    app = QApplication([])
    window = QWidget()
    window.setGeometry(100,100,200,300)
    window.setWindowTitle("Test app")

    layout = QVBoxLayout()
    label = QLabel("Press the button bellow")
    button = QPushButton("Press me!")
    button.pressed.connect(on_clicked)

    layout.addWidget(label)
    layout.addWidget(button)

    window.setLayout(layout)

    window.show()
    app.exec()

if __name__ == '__main__':
    main()