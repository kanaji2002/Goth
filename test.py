import os
import sys
import re
import asyncio
import aiohttp
import threading
import xml.etree.ElementTree as ET
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtWebEngineWidgets import *
from PySide6.QtWebEngineCore import QWebEngineProfile
import yt_dlp
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # タブを追加
        self.addTab("Tab 1", "This is Tab 1")
        self.addTab("Tab 2", "This is Tab 2")
        self.addTab("Tab 3", "This is Tab 3")

        # QShortcut の定義
        self.setup_shortcuts()

    def addTab(self, title, content):
        new_widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel(content)
        layout.addWidget(label)
        new_widget.setLayout(layout)
        self.tabs.addTab(new_widget, title)
        self.tabs.setTabsClosable(True)

    def setup_shortcuts(self):
        # Ctrl+W で現在のタブを閉じる
        close_tab_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        close_tab_shortcut.activated.connect(self.close_current_tab)

        # Ctrl+Space で現在のタブを閉じる
        close_tab_shortcut = QShortcut(QKeySequence("Ctrl+Space"), self)
        close_tab_shortcut.activated.connect(self.close_two_tab)

        # Ctrl+T で新しいタブを開く
        new_tab_shortcut = QShortcut(QKeySequence("Ctrl+T"), self)
        new_tab_shortcut.activated.connect(self.add_new_tab)

        # Ctrl+Q でアプリケーションを終了する
        quit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        quit_shortcut.activated.connect(self.close)

        # Alt+LeftArrow で前のタブに移動する
        prev_tab_shortcut = QShortcut(QKeySequence(Qt.ALT + Qt.Key_Left), self)
        prev_tab_shortcut.activated.connect(self.prev_tab)

        # Alt+RightArrow で次のタブに移動する
        next_tab_shortcut = QShortcut(QKeySequence(Qt.ALT + Qt.Key_Right), self)
        next_tab_shortcut.activated.connect(self.next_tab)

    def close_current_tab(self):
        current_index = self.tabs.currentIndex()
        if current_index != -1:
            self.tabs.removeTab(current_index)

    def close_two_tab(self):
        current_index = self.tabs.currentIndex()
        if current_index != -1:
            self.tabs.removeTab(current_index)
            self.tabs.removeTab(current_index)

    

    def add_new_tab(self):
        self.addTab(f"New Tab {self.tabs.count() + 1}", f"This is new tab {self.tabs.count() + 1}")

    def prev_tab(self):
        current_index = self.tabs.currentIndex()
        if current_index > 0:
            self.tabs.setCurrentIndex(current_index - 1)

    def next_tab(self):
        current_index = self.tabs.currentIndex()
        if current_index < self.tabs.count() - 1:
            self.tabs.setCurrentIndex(current_index + 1)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
