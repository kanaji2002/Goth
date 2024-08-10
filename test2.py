from PySide6.QtCore import QObject, Signal, Slot
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
        
        # スタイルシートを適用（前述のコード）
        self.tabs.setStyleSheet("""
            QTabBar::tear { width: 0; height: 0; }
            QTabWidget::pane { border-top: 2px solid #C2C7CB; position: absolute; top: -0.5em; }
            QTabBar { qproperty-drawBase: 0; left: 5px; } 
            QTabBar::tab { background: lightgray; border: 1px solid #C4C4C3; border-bottom-color: #C2C7CB; border-top-left-radius: 4px; border-top-right-radius: 4px; padding: 5px; }
            QTabBar::tab:selected, QTabBar::tab:hover { background: white; }
        """)

        # タブウィジェットを中央ウィジェットとして設定
        self.setCentralWidget(self.tabs)
        
        
   
        
        
    def create_database(self):
        if not os.path.exists('shortcuts.xml'):
            root = ET.Element("shortcuts")
            tree = ET.ElementTree(root)
            tree.write('shortcuts.xml')

app = QApplication(sys.argv)
app.setApplicationName("OrbBrowser")
window = MainWindow()
window.create_database()
window.show()
app.exec()
