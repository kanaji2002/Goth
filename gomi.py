from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QToolBar, QPushButton, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt, QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.vertical_bar = QToolBar("Vertical Bar")
        self.vertical_bar.setOrientation(Qt.Orientation.Vertical)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.vertical_bar)
        
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)

        self.add_tab_button = QPushButton("+aaaaaaaaa")
        self.add_tab_button.clicked.connect(self.add_new_tab)
        self.add_tab_button.setStyleSheet("background-color: white; color: pink;")
        self.tabs.setCornerWidget(self.add_tab_button, Qt.TopRightCorner)

        self.tabs.setStyleSheet("""
            QTabBar::tear { width: 0; height: 0; }
            QTabWidget::pane { border-top: 2px solid #C2C7CB; position: absolute; top: -0.5em; }
            QTabBar { qproperty-drawBase: 0; left: 5px; }
            QTabBar::tab { background: lightgray; border: 1px solid #C4C4C3; border-bottom-color: #C2C7CB; border-top-left-radius: 4px; border-top-right-radius: 4px; padding: 5px; }
            QTabBar::tab:selected, QTabBar::tab:hover { background: white; }
        """)

        self.setCentralWidget(self.tabs)

        self.add_new_tab()

    def tab_open_doubleclick(self, index):
        if index == -1:
            self.add_new_tab()

    def current_tab_changed(self, index):
        current_widget = self.tabs.widget(index)
        if isinstance(current_widget, QWebEngineView):
            print(f"Current tab changed to: {current_widget.url().toString()}")

    def add_new_tab(self, qurl=None, label="ブランク"):
        if qurl is None:
            qurl = QUrl('https://kanaji2002.github.io/Goth-toppage/top_page.html')
        elif isinstance(qurl, str):
            qurl = QUrl(qurl)
        
        browser = QWebEngineView()
        browser.setUrl(qurl)
        
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tabs.setTabText(
            i, browser.page().title()[:7] if len(browser.page().title()) > 7 else browser.page().title().ljust(7)
        ))
        browser.iconChanged.connect(lambda _, i=i, browser=browser: self.tabs.setTabIcon(i, browser.icon()))

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
