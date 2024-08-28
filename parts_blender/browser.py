import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class WebSearchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web Search Application")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create search input and button
        self.search_input = QLineEdit()
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.perform_search)
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)

        # Create WebEngineView to display the HTML file
        self.web_view = QWebEngineView()
        self.web_view.load(QUrl.fromLocalFile("test.html"))
        layout.addWidget(self.web_view)

    def perform_search(self):
        query = self.search_input.text()
        # Call the JavaScript function in the HTML file
        self.web_view.page().runJavaScript(f"search('{query}')")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WebSearchApp()
    window.show()
    sys.exit(app.exec_())