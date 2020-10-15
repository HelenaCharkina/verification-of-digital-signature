import sys
import json

import cv2
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLabel, QPushButton, QScrollArea, QLineEdit, \
    QVBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap, QPainter

#import cv2

#from neural.GetString import get_string
from router import sign, check


class AppCall:
    def __init__(self, app, index):
        self.app = app
        self.index = index
    
    def __call__(self):
        self.app.set_active_field(self.index)

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Проверка подписи'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.field_buttons = []
        self.file_name = ""

        self.initUI()
    
    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)        

        self.layout = QVBoxLayout()
        self.layout.stretch(1)

        imageLabel = QLabel(self)
        scrollArea = QScrollArea()
        scrollArea.setWidget(imageLabel)

        self.layout.addWidget(scrollArea)
        self.image = imageLabel
        self.setLayout(self.layout)

        # widget = QLineEdit()
        # widget.textChanged.connect(self.on_field_edited)
        # self.layout.addWidget(widget)
        # self.editor = widget

        widget = QPushButton('Выбрать изображение')
        widget.setToolTip('Выбрать изображение для проверки подписи')
        widget.clicked.connect(self.select_image)
        self.layout.addWidget(widget)

        widget = QPushButton('Проверить подпись')
        widget.setToolTip('Выбрать изображение для проверки подписи')
        widget.clicked.connect(self.check_image)
        self.layout.addWidget(widget)

        widget = QPushButton('Подписать')
        widget.setToolTip('Добавить подпись в изображение')
        widget.clicked.connect(self.sign_image)
        self.layout.addWidget(widget)

        # widget = QPushButton('Сохранить')
        # widget.setToolTip('Сохранить изображение')
        # widget.clicked.connect(self.save_image)
        # self.layout.addWidget(widget)



        self.button_style = """
            QPushButton {
                color: rgb(0,64,0);
                border: 2px solid rgba(128,128,128,20);
                background: rgba(0,0,0,20);
                text-align: left;
            }
            QPushButton:hover  {
                color: rgb(0, 255, 0);
                border: 2px solid rgba(0,255,0,20);
                background: rgba(0,255,0,20);
                text-align: left;
            }
            QPushButton:pressed  {
                color: rgb(0, 128, 0);
                border: 2px solid rgba(0,255,0,40);
                background: rgba(0,255,0,40);
                text-align: left;
            }
         """

        with open("coordinates.json") as f:
            self.coordinates = json.load(f)
        self.field_values = []
        self.s = ""
        self.r = ""

        self.show()

    def on_field_edited(self, s):
        if self.active_field is None:
            return
        print(self.active_field)
        self.field_values[self.active_field] = s
        self.field_buttons[self.active_field].setToolTip(s)

    def initialize_field_values(self):
        self.s = ""
        self.r = ""
        self.field_values = ["" for i in self.coordinates['fields']]

    def set_active_field(self, index):
        print(index, len(self.field_values))
        self.active_field = index
        self.editor.setText(self.field_values[index])

    def update_button_fields(self):
        for button in self.field_buttons:
            button.deleteLater()
        self.field_buttons = []
        size = self.image.pixmap().width()

        self.initialize_field_values()

        index = 0
        for coord in self.coordinates['fields']:
            button = QPushButton(str(index + 1), self.image)
            button.clicked.connect(AppCall(self, index))
            button.setStyleSheet(self.button_style)
            button.move(int(coord['x'] * size), int(coord['y'] * size))
            button.resize(int(coord['width'] * size), int(coord['height'] * size))
            button.setToolTip(self.field_values[index])
            button.show()
            self.field_buttons.append(button)
            index += 1

        self.repaint()
        self.image.repaint()
        self.show()

    def sign_image(self):
        sign(self.file_name)
        pm = QPixmap("signed_images/sign.jpg")
        # self.cvimage = cv2.imread(file_name)
        self.image.setPixmap(pm)
        self.image.repaint()
        self.repaint()
        self.image.resize(pm.width(), pm.height())
        self.update_button_fields()
        self.resize(pm.width(), pm.height())


    def check_image(self):
        ok = check(self.file_name)
        msg = QMessageBox()
        msg.setWindowTitle("Результат")
        if ok:
            msg.setText("Подпись верна!")
        else:
            msg.setText("Подпись не верна!")
        msg.exec_()


    def select_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "All Image Files ()", options=options)
        if file_name:
            self.file_name = file_name
            pm = QPixmap(file_name)
            #self.cvimage = cv2.imread(file_name)
            self.image.setPixmap(pm)
            self.image.repaint()
            self.repaint()
            self.image.resize(pm.width(), pm.height())
            self.update_button_fields()
            self.resize(pm.width(), pm.height())

    def save_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить изображение", "", "All Image Files (*.jpg, *.png)", options=options)
        if file_name:
            pass


app = QApplication(sys.argv)
ex = App()
sys.exit(app.exec_())


