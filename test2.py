from PySide6.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QPushButton, QWidget

app = QApplication([])

window = QWidget()
main_layout = QVBoxLayout()

# サブレイアウトを作成
sub_layout = QHBoxLayout()
button1 = QPushButton('Button 1')
button2 = QPushButton('Button 2')
sub_layout.addWidget(button1)
sub_layout.addWidget(button2)

# サブレイアウトをメインレイアウトに追加
main_layout.addLayout(sub_layout)

# 別のボタンをメインレイアウトに追加
button3 = QPushButton('Button 3')
main_layout.addWidget(button3)

window.setLayout(main_layout)
window.show()

app.exec()
