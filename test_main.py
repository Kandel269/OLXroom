import pytest
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QLineEdit
from pytestqt import qtbot

from main import OLXWork, OLXSettings
from PyQt6 import QtCore


def test_olxwork_button_stop_clicked(qtbot):
    parent = OLXSettings()
    widget = OLXWork(parent= parent)
    widget.show()
    qtbot.addWidget(widget)
    assert widget.isVisible()

    widget.start_timer()
    qtbot.mouseClick(widget.button_stop, QtCore.Qt.MouseButton.LeftButton)

    assert not widget.isVisible()
    assert parent.isVisible()

def test_olxwork_animation_label(qtbot):
    widget = OLXWork()
    assert widget.in_progress_label.text() == "Program w trakcie pracy"
    widget.animation_label_counter = 0
    widget.animation_label()
    assert widget.in_progress_label.text() == "Program w trakcie pracy."
    for _ in range(3):
        widget.animation_label()
    assert widget.in_progress_label.text() == "Program w trakcie pracy"

def test_olxwork_start_timer(qtbot):
    widget = OLXWork()
    qtbot.addWidget(widget)
    widget.start_timer()
    assert widget.animation_label_timer.isActive()
    assert widget.room_olx_timer.isActive()

def test_olxwork_stop_timer(qtbot):
    widget = OLXWork()
    qtbot.addWidget(widget)
    widget.start_timer()
    widget.stop_timer()
    assert not widget.animation_label_timer.isActive()
    assert not widget.room_olx_timer.isActive()

def test_olxwork_update_data_olxwork(qtbot):
    widget = OLXWork()
    qtbot.addWidget(widget)
    widget.update_data_olxwork("http://something.pl","City")
    assert widget.city == "City"
    assert widget.url == "http://something.pl"

def test_olxsettings_button_start_clicked(qtbot):
    widget = OLXSettings()
    son = OLXWork(parent=widget)
    widget.olx_work = son
    qtbot.keyClicks(widget.city, "Zakopane")
    widget.show()
    assert widget.isVisible()
    qtbot.addWidget(widget)
    qtbot.mouseClick(widget.button_start,QtCore.Qt.MouseButton.LeftButton)
    assert son.isVisible()
    assert not widget.isVisible()

def test_olxsettings_check_city(qtbot):
    widget = OLXSettings()
    widget.city = QLineEdit()
    widget.city.setText("Warszawa")
    assert widget.check_city() == 0

def test_olxsettings_check_city_empty(qtbot):
    widget = OLXSettings()
    widget.city = QLineEdit()
    widget.city.setText("")
    assert widget.check_city() == 1

def test_olxsettings_check_city_invalid(qtbot):
    widget = OLXSettings()
    widget.city = QLineEdit()
    widget.city.setText("InvalidCity")
    assert widget.check_city() == 1

def test_olxsettings_main_window_type_index_changed_visible(qtbot):
    widget = OLXSettings()
    qtbot.addWidget(widget)
    widget.show()
    assert widget.type.currentIndex() == 0
    assert not widget.rooms.isVisible()
    assert not widget.rooms_label.isVisible()
    assert widget.m_2_from.isVisible()
    assert widget.m_2_to.isVisible()


    qtbot.waitUntil(lambda: widget.type.count() > 0)
    qtbot.mouseClick(widget.type, QtCore.Qt.MouseButton.LeftButton)
    qtbot.keyClick(widget.type, QtCore.Qt.Key.Key_Down)
    qtbot.keyClick(widget.type, QtCore.Qt.Key.Key_Return)
    assert widget.rooms.isVisible()
    assert widget.rooms_label.isVisible()
    assert widget.m_2_from.isVisible()
    assert widget.m_2_to.isVisible()

    qtbot.waitUntil(lambda: widget.type.count() > 0)
    qtbot.mouseClick(widget.type, QtCore.Qt.MouseButton.LeftButton)
    qtbot.keyClick(widget.type, QtCore.Qt.Key.Key_Down)
    qtbot.keyClick(widget.type, QtCore.Qt.Key.Key_Return)
    assert not widget.rooms.isVisible()
    assert not widget.rooms_label.isVisible()
    assert not widget.m_2_from.isVisible()
    assert not widget.m_2_to.isVisible()