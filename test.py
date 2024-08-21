from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QUrl, Qt

import sys

    
    
    
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

class CustomWebEnginePage(QWebEnginePage):
    def createWindow(self, _type):
        # 新しい QWebEngineView を作成
        popup = QWebEngineView()
        popup.setAttribute(Qt.WA_DeleteOnClose, True)

        # 新しいページを作成してビューに設定
        new_page = CustomWebEnginePage(popup)
        popup.setPage(new_page)

        # ポップアップウィンドウを表示
        popup.show()

        # 新しい QWebEnginePage を返す
        return new_page

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web View Example")

        # QWebEngineView の設定
        self.web_view = QWebEngineView()
        self.web_page = CustomWebEnginePage(self.web_view)
        self.web_view.setPage(self.web_page)
        self.setCentralWidget(self.web_view)

        # ローカルHTMLファイルまたはURLを設定
        self.web_view.setUrl(QUrl("file:///toppage/top_page.html"))  # ここにファイルのパスを指定

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

