from PySide6.QtWidgets import *
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt

from PIL import Image, ImageEnhance, ImageFilter
import os
import sys

path = './imgs/duck.jpeg'
fixed_image_size = (400, 400)

original_image = None
modified_image = None
backup_image = None

brightness_factor = 1.0
contrast_factor = 1.0

initial_brightness_factor = 1.0
initial_contrast_factor = 1.0

brightness_slider = None
contrast_slider = None

def apply_initial_state():
    global modified_image, backup_image, initial_brightness_factor, initial_contrast_factor
    modified_image = original_image.copy()
    backup_image = modified_image.copy()
    initial_brightness_factor = 1.0
    initial_contrast_factor = 1.0
    update_brightness_slider(1.0)
    update_contrast_slider(1.0)
    apply_brightness_contrast()

def update_brightness_slider(value):
    global brightness_slider
    brightness_slider.blockSignals(True)
    brightness_slider.setValue(int(value * 100))
    brightness_slider.blockSignals(False)

def update_contrast_slider(value):
    global contrast_slider
    contrast_slider.blockSignals(True)
    contrast_slider.setValue(int(value * 100))
    contrast_slider.blockSignals(False)

def rotate90():
    global modified_image, backup_image
    if modified_image:
        backup_image = modified_image.copy()
        modified_image = modified_image.rotate(90)
        update_image_label()

def rotateneg90():
    global modified_image, backup_image
    if modified_image:
        backup_image = modified_image.copy()
        modified_image = modified_image.rotate(-90)
        update_image_label()

def grayscale_image():
    global modified_image, backup_image
    if modified_image:
        backup_image = modified_image.copy()
        modified_image = modified_image.convert('L')
        update_image_label()

def undo_changes():
    global modified_image, backup_image
    if backup_image:
        modified_image = backup_image.copy()
        update_image_label()

def update_brightness(value):
    global brightness_factor
    brightness_factor = max(value, 0.01)
    apply_brightness_contrast()

def update_contrast(value):
    global contrast_factor
    contrast_factor = value
    apply_brightness_contrast()

def apply_brightness_contrast():
    global modified_image, backup_image
    if modified_image:
        backup_image = modified_image.copy()
        temp_image = original_image.copy()
        enhancer = ImageEnhance.Brightness(temp_image)
        modified_image = enhancer.enhance(initial_brightness_factor * brightness_factor)
        enhancer = ImageEnhance.Contrast(modified_image)
        modified_image = enhancer.enhance(initial_contrast_factor * contrast_factor)
        update_image_label()

def update_image_label():
    img = modified_image.copy() if modified_image else None
    if img:
        img.thumbnail(fixed_image_size)
        qimage = QImage(img.tobytes(), img.width, img.height, img.width * 3, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        image_label.setPixmap(pixmap)

def change_image_path():
    global path, original_image, modified_image, backup_image, initial_brightness_factor, initial_contrast_factor
    file_dialog = QFileDialog()
    new_path, _ = file_dialog.getOpenFileName(None, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")
    if new_path:
        path = new_path
        original_image = Image.open(path)
        initial_state_button.setEnabled(True)
        initial_brightness_factor = 1.0
        initial_contrast_factor = 1.0
        update_brightness_slider(1.0)
        update_contrast_slider(1.0)
        apply_initial_state()
        update_image_label()

def export_image():
    global modified_image
    if modified_image:
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(None, "Save Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_path:
            modified_image.save(file_path)

def main():
    global image_label, original_image, modified_image, backup_image, \
           initial_state_button, brightness_slider, contrast_slider

    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Photo Editor")
    window.setGeometry(100, 100, 400, 500)

    # Create buttons
    rotate90_button = QPushButton("Rotate 90")
    rotateneg90_button = QPushButton("Rotate -90")
    grayscale_button = QPushButton("Grayscale")
    undo_button = QPushButton("Undo Last Change")
    change_button = QPushButton("Upload Image")
    initial_state_button = QPushButton("Restore Initial State")
    export_button = QPushButton("Export Image")

    # Connect button signals to functions
    rotate90_button.clicked.connect(rotate90)
    rotateneg90_button.clicked.connect(rotateneg90)
    grayscale_button.clicked.connect(grayscale_image)
    undo_button.clicked.connect(undo_changes)
    change_button.clicked.connect(change_image_path)
    initial_state_button.setEnabled(False)
    initial_state_button.clicked.connect(apply_initial_state)
    export_button.clicked.connect(export_image)

    # Create sliders
    brightness_slider = QSlider(Qt.Horizontal)
    contrast_slider = QSlider(Qt.Horizontal)

    # Set slider properties
    brightness_slider.setMinimum(0)
    brightness_slider.setMaximum(200)
    brightness_slider.setValue(100)
    brightness_slider.valueChanged.connect(lambda value: update_brightness(value / 100))

    contrast_slider.setMinimum(0)
    contrast_slider.setMaximum(200)
    contrast_slider.setValue(100)
    contrast_slider.valueChanged.connect(lambda value: update_contrast(value / 100))

    # Create layout for sliders
    slider_layout = QVBoxLayout()
    slider_layout.addWidget(QLabel("Brightness"))
    slider_layout.addWidget(brightness_slider)
    slider_layout.addWidget(QLabel("Contrast"))
    slider_layout.addWidget(contrast_slider)

    # Create layout for buttons
    button_layout = QHBoxLayout()
    button_layout.addWidget(rotate90_button)
    button_layout.addWidget(rotateneg90_button)
    button_layout.addWidget(grayscale_button)
    button_layout.addWidget(undo_button)
    button_layout.addWidget(change_button)
    button_layout.addWidget(initial_state_button)
    button_layout.addWidget(export_button)

    # Create image label
    image_label = QLabel()
    update_image_label()

    # Create main layout
    main_layout = QVBoxLayout()
    main_layout.addLayout(button_layout)
    main_layout.addLayout(slider_layout)
    main_layout.addWidget(image_label)

    # Set main layout for central widget
    container = QWidget()
    container.setLayout(main_layout)
    window.setCentralWidget(container)

    # Show the window
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
