from PySide6.QtCore import QObject, Signal, Slot

class Button(QObject):
    # シグナルの定義（引数として文字列を持つ）
    clicked = Signal(str)

    def __init__(self):
        super().__init__()

    def click(self):
        # シグナルの発行
        self.clicked.emit("Button was clicked!")

class Handler(QObject):
    def __init__(self):
        super().__init__()

    # スロットの定義
    @Slot(str)
    def on_button_clicked(self, message):
        print(message)

# オブジェクトの作成
button = Button()
handler = Handler()

# シグナルとスロットの接続
button.clicked.connect(handler.on_button_clicked)

# ボタンがクリックされたことをシミュレート
button.click()
