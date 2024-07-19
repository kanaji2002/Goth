import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QLineEdit, QPushButton, QTabWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Simple Browser')
        self.setGeometry(100, 100, 1024, 768)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.create_toolbar()
        self.add_new_tab()

    def create_toolbar(self):
        navbar = QToolBar()
        self.addToolBar(navbar)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        search_button = QPushButton('Search')
        search_button.clicked.connect(self.search)
        navbar.addWidget(search_button)

    def add_new_tab(self, qurl=None):
        if qurl is None:
            qurl = QUrl('https://www.google.com')

        browser = QWebEngineView()
        browser.setUrl(qurl)

        i = self.tabs.addTab(browser, 'New Tab')
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))

        if qurl == QUrl('https://www.google.com'):
            browser.page().loadFinished.connect(self.inject_js)

    def navigate_to_url(self):
        q = QUrl(self.url_bar.text())
        if q.scheme() == '':
            q.setScheme('http')
        self.tabs.currentWidget().setUrl(q)

    def update_urlbar(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            return
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

    def search(self):
        search_term = self.url_bar.text()
        search_url = QUrl(f'https://www.google.com/search?q={search_term}')
        self.add_new_tab(search_url)

    def inject_js(self):
        js_code = """
        var script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js';
        script.onload = function() {
            var overlay = document.createElement('div');
            overlay.style.position = 'fixed';
            overlay.style.top = '0';
            overlay.style.left = '0';
            overlay.style.width = '100%';
            overlay.style.height = '100%';
            overlay.style.pointerEvents = 'none';
            document.body.appendChild(overlay);

            var scene = new THREE.Scene();
            var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            var renderer = new THREE.WebGLRenderer({ alpha: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            overlay.appendChild(renderer.domElement);

            var geometry = new THREE.BoxGeometry();
            var material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
            var mesh = new THREE.Mesh(geometry, material);
            scene.add(mesh);

            camera.position.z = 5;

            function animate() {
                requestAnimationFrame(animate);
                mesh.rotation.x += 0.01;
                mesh.rotation.y += 0.01;
                renderer.render(scene, camera);
            }
            animate();
        };
        document.head.appendChild(script);
        """

        current_page = self.tabs.currentWidget().page()
        current_page.runJavaScript(js_code)

app = QApplication(sys.argv)
window = Browser()
window.show()
sys.exit(app.exec_())
