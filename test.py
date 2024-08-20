from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QLabel, QWidget
from PySide6.QtCore import Qt, QEvent
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # タブバーのイベントフィルタを設定
        self.tabs.tabBar().installEventFilter(self)

        # タブが閉じられたときのシグナルを接続
        self.tabs.tabCloseRequested.connect(self.close_tab)

        # タブを追加
        self.addTab("Tab 1", "This is Tab 1")
        self.addTab("Tab 2", "This is Tab 2")
        self.addTab("Tab 3", "This is Tab 3")

        # 左ボタンが押されたかどうかを保持するフラグ
        self.left_button_pressed = False

    def addTab(self, title, content):
        new_widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel(content)
        layout.addWidget(label)
        new_widget.setLayout(layout)
        self.tabs.addTab(new_widget, title)
        self.tabs.setTabsClosable(True)

    def eventFilter(self, obj, event):
        if obj == self.tabs.tabBar():
            if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
                self.left_button_pressed = True
            elif event.type() == QEvent.MouseButtonRelease:
                self.left_button_pressed = False
        return super().eventFilter(obj, event)

    def close_tab(self, i):
        if self.left_button_pressed and self.tabs.count() > 1:
            self.tabs.removeTab(i)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
