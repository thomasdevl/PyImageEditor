from PySide6.QtWidgets import *
from PySide6.QtGui import QPixmap, QImage
from PIL import Image, ImageEnhance, ImageFilter
import os
import sys

path = './imgs/duck.jpeg'
fixed_image_size = (400, 400)  # Set your desired fixed size here

def rotate90():
    img = Image.open(path)
    edit = img.rotate(90)
    edit.save(path)
    update_image_label()

def rotateneg90():
    img = Image.open(path)
    edit = img.rotate(-90)
    edit.save(path)
    update_image_label()

def update_image_label():
    img = Image.open(path)
    img.thumbnail(fixed_image_size)
    qimage = QImage(img.tobytes(), img.width, img.height, img.width * 3, QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(qimage)
    image_label.setPixmap(pixmap)

def change_image_path():
    global path
    file_dialog = QFileDialog()
    new_path, _ = file_dialog.getOpenFileName(None, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")
    if new_path:
        path = new_path
        update_image_label()

def main():
    global image_label

    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Photo Editor")
    window.setGeometry(100, 100, 200, 300)
    
    rbutton = QPushButton("Rotate 90")
    rbutton.pressed.connect(rotate90)
    lbutton = QPushButton("Rotate -90")
    lbutton.pressed.connect(rotateneg90)
    change_button = QPushButton("Change Image")
    change_button.pressed.connect(change_image_path)

    button_layout = QHBoxLayout()
    button_layout.addWidget(rbutton)
    button_layout.addWidget(lbutton)
    button_layout.addWidget(change_button)

    image_label = QLabel()
    update_image_label()
    
    main_layout = QVBoxLayout()
    main_layout.addLayout(button_layout)
    main_layout.addWidget(image_label)

    container = QWidget()
    container.setLayout(main_layout)
    window.setCentralWidget(container)

    window.show()
    app.exec()

if __name__ == '__main__':
    main()
