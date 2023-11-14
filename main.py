import sys
from functools import partial

from PyQt6.QtCore import QTimer, QUrl
from PyQt6.QtGui import QIcon, QIntValidator, QDesktopServices
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QVBoxLayout, QComboBox, QLineEdit, \
    QListWidget, QListWidgetItem, QCheckBox, QLabel, QGridLayout

from url import *

class OLXWork(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("OLX mieszkania - praca")
        self.setFixedSize(800, 600)

        self.icon = QIcon(f"image/icon_64.png")
        self.setWindowIcon(self.icon)

        self.ignore_close_event = False

        self.main_window()

    def start_timer(self) -> None:
        self.animation_label_timer = QTimer(self)
        self.animation_label_timer.timeout.connect(self.animation_label)
        self.animation_label_counter = 0
        self.animation_label_timer.start(500)

        self.room_olx_timer = QTimer(self)
        self.room_olx_timer.timeout.connect(self.room_olx)
        self.room_olx_timer.start(900000)

    def stop_timer(self) -> None:
        self.animation_label_timer.stop()
        self.room_olx_timer.stop()

    def room_olx(self) -> None:
        self.current_time, room_list = get_room_olx(self.url,self.city, self.current_time)

        for room in room_list:
            item = QListWidgetItem()
            url = OLX_URL + room[0]
            room_button = QPushButton(f"{room[1]}: {url}")
            room_button.setFlat(True)
            room_button.setStyleSheet("text-align:left; padding:0px; color: blue; text-decoration: underline;")
            room_button.clicked.connect(partial(QDesktopServices.openUrl, QUrl(url)))
            self.new_room_list.insertItem(0, item)
            self.new_room_list.setItemWidget(item, room_button)
            item.setSizeHint(room_button.sizeHint())

    def animation_label(self) -> None:
        self.animation_label_counter += 1
        if self.animation_label_counter > 3:
            self.animation_label_counter = 0
        repeated_point = "." * self.animation_label_counter
        self.in_progress_label.setText(f"Program w trakcie pracy{repeated_point}")

    def main_window(self) -> None:
        self.button_stop = QPushButton("Zatrzymaj program")
        self.button_stop.clicked.connect(self.button_stop_clicked)

        self.in_progress_label = QLabel("Program w trakcie pracy")

        self.new_room_list = QListWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.in_progress_label)
        layout.addWidget(self.new_room_list)
        layout.addWidget(self.button_stop)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def button_stop_clicked(self) -> None:
        self.ignore_close_event = True
        self.close()
        self.ignore_close_event = False
        self.parent().show()

    def update_data_olxwork(self, url:str, city:str) -> None:
        self.url = url
        self.city = city
        now = datetime.now()
        self.current_time = now.time()

    def closeEvent(self, event) -> None:
        self.stop_timer()
        if not self.ignore_close_event:
            sys.exit()

class OLXSettings(QMainWindow):
    def __init__(self):
        super().__init__()

        self.url = None
        self.olx_work = None
        self.city_edited = None
        self.setWindowTitle("OLX mieszkania - ustawienia")
        self.setFixedSize(800, 600)

        self.icon = QIcon(f"image/icon_64.png")
        self.setWindowIcon(self.icon)
        self.main_window()

    def type_index_changed(self, index:int) -> None:
        subcategory_is_visible = index == 0 or index == 1
        self.subcategory_label.setVisible(subcategory_is_visible)
        self.subcategory.setVisible(subcategory_is_visible)

        self.rooms_label.setVisible(index == 1)
        self.rooms.setVisible(index == 1)

        m_2_is_visible = index == 0 or index == 1
        self.m_2_to_label.setVisible(m_2_is_visible)
        self.m_2_to.setVisible(m_2_is_visible)
        self.m_2_from_label.setVisible(m_2_is_visible)
        self.m_2_from.setVisible(m_2_is_visible)

    def check_city(self) -> bool:
        city = self.city.text()
        if not city:
            return 1
        city_lower = city.lower()
        self.city_edited = city_lower.replace("ą","a").replace("ę","e").replace("ł","l").replace("ź","z").replace("ż","z").replace("ć","c").replace("ń","n").replace("ó","o")
        try_city = OLX_URL + self.city_edited + "/"
        html_text = requests.get(try_city).text
        soup = BeautifulSoup(html_text, 'lxml')
        try:
            if soup.find("div", class_="c-container"):
                return 1
            else:
                return 0
        except:
            return 0

    def button_start_clicked(self) -> None:
        if self.check_city():
            self.city_error_label.setVisible(True)
            return
        else:
            self.city_error_label.setVisible(False)

        if not self.olx_work:
            self.olx_work = OLXWork(parent=self)

        self.update_data_olxwork()
        self.olx_work.show()
        self.hide()

    def update_data_olxwork(self) -> None:
        selected_rooms = []
        for index in range(self.rooms.count()):
            item = self.rooms.item(index)
            check_box = self.rooms.itemWidget(item)
            if check_box.isChecked():
                selected_rooms.append(check_box.text())

        type = self.type.currentText()
        city = self.city.text().capitalize()
        m_2_from = self.m_2_from.text().replace("-", "")
        m_2_to = self.m_2_to.text().replace("-", "")
        price_from = self.price_from.text().replace("-", "")
        price_to = self.price_to.text().replace("-", "")
        subcategory = self.subcategory.currentText().lower()
        self.url = create_url(type=type, city=self.city_edited, rooms=selected_rooms, m_2_from=m_2_from, m_2_to=m_2_to,
                              price_from=price_from, price_to=price_to, subcategory=subcategory)
        self.olx_work.update_data_olxwork(self.url, city)
        self.olx_work.start_timer()

    def button_exit_clicked(self)  -> None:
        self.close()

    def handle_destroy_olx_work(self, obj:object)  -> None:
        if obj == self.olx_work:
            sys.exit()

    def main_window(self) -> None:
        self.int_validator = QIntValidator()

        self.button_start = QPushButton("Start")
        self.button_start.clicked.connect(self.button_start_clicked)

        self.button_exit = QPushButton("Wyjście")
        self.button_exit.clicked.connect(self.button_exit_clicked)

        self.type_label = QLabel("Wybierz rodzaj nieruchomości")
        self.type = QComboBox()
        self.type.addItems(["domy","mieszkania", "stancje-pokoje"])
        self.type.currentIndexChanged.connect(self.type_index_changed)

        self.city_label = QLabel("Wpisz interesującą ciebie miejscowość")
        self.city = QLineEdit()
        self.city.setPlaceholderText("Podaj miejscowość")
        self.city_error_label = QLabel("Podane miasto jest nieprawidłowe")
        self.city_error_label.setStyleSheet("color: red;")
        self.city_error_label.setVisible(False)

        self.rooms = QListWidget()
        self.rooms_label = QLabel("Wybierz liczbę pokoi (domyślnie wszystkie)")
        options_rooms = ["Kawalerka", "2 pokoje", "3 pokoje", "4 i więcej"]
        for option in options_rooms:
            item = QListWidgetItem()
            check_box = QCheckBox(option)
            self.rooms.addItem(item)
            self.rooms.setItemWidget(item, check_box)
            item.setSizeHint(check_box.sizeHint())
        self.rooms_label.setVisible(self.type.currentIndex() == 1)
        self.rooms.setVisible(self.type.currentIndex() == 1)

        self.m_2_from_label = QLabel("Podaj interesujący ciebie minimalny metraż")
        self.m_2_from = QLineEdit()
        self.m_2_from.setValidator(self.int_validator)
        self.m_2_from .setPlaceholderText("0")
        self.m_2_from_label.setVisible(self.type.currentIndex() == 0 or self.type.currentIndex() == 1)
        self.m_2_from.setVisible(self.type.currentIndex() == 0 or self.type.currentIndex() == 1)

        self.m_2_to_label = QLabel("Podaj interesujący ciebie maksymalny metraż")
        self.m_2_to = QLineEdit()
        self.m_2_to.setValidator(self.int_validator)
        self.m_2_to.setPlaceholderText("0")
        self.m_2_to_label.setVisible(self.type.currentIndex() == 0 or self.type.currentIndex() == 1)
        self.m_2_to.setVisible(self.type.currentIndex() == 0 or self.type.currentIndex() == 1)

        self.price_from_label = QLabel("Podaj interesującą ciebie minimalną kwotę")
        self.price_from = QLineEdit()
        self.price_from.setValidator(self.int_validator)
        self.price_from .setPlaceholderText("0")

        self.price_to_label = QLabel("Podaj interesującą ciebie maksymalną kwotę")
        self.price_to = QLineEdit()
        self.price_to.setValidator(self.int_validator)
        self.price_to.setPlaceholderText("0")

        self.subcategory_label = QLabel("Wybierz interesującą ciebie kategorię")
        self.subcategory = QComboBox()
        self.subcategory.addItems(["Wynajem","Sprzedaż", "Zamiana"])
        self.subcategory.setVisible(self.type.currentIndex() in [0, 1])
        self.subcategory_label.setVisible(self.type.currentIndex() in [0, 1])

        self.message = QListWidget()
        self.message_label = QLabel("Wybierz rodzaj powiadomień")
        options_message = ["e-mail","w oknie programu","sms"]
        for option in options_message:
            item = QListWidgetItem()
            check_box = QCheckBox(option)
            self.message.addItem(item)
            self.message.setItemWidget(item, check_box)
            item.setSizeHint(check_box.sizeHint())

            check_box.setDisabled(True)
            if option == "w oknie programu":
                check_box.setChecked(True)


        main_layout = QVBoxLayout()
        layout_grid = QGridLayout()

        main_layout.addWidget(self.type_label)
        main_layout.addWidget(self.type)
        main_layout.addWidget(self.city_label)
        main_layout.addWidget(self.city)
        main_layout.addWidget(self.city_error_label)
        main_layout.addWidget(self.rooms_label)
        main_layout.addWidget(self.rooms)

        layout_grid.addWidget(self.m_2_from_label, 0,0)
        layout_grid.addWidget(self.m_2_from,1,0)
        layout_grid.addWidget(self.m_2_to_label,0,1)
        layout_grid.addWidget(self.m_2_to,1,1)
        layout_grid.addWidget(self.price_from_label,2,0)
        layout_grid.addWidget(self.price_from,3,0)
        layout_grid.addWidget(self.price_to_label,2,1)
        layout_grid.addWidget(self.price_to,3,1)
        main_layout.addLayout(layout_grid)

        main_layout.addWidget(self.subcategory_label)
        main_layout.addWidget(self.subcategory)
        main_layout.addWidget(self.message_label)
        main_layout.addWidget(self.message)
        main_layout.addWidget(self.button_start)
        main_layout.addWidget(self.button_exit)

        widget = QWidget()
        widget.setLayout(main_layout)

        self.setCentralWidget(widget)

        if self.olx_work:
            self.olx_work.destroyed.connect(self.handle_destroy_olx_work)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OLXSettings()
    window.show()
    app.exec()
    sys.exit()





