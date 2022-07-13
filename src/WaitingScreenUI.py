from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout


class WaitingScreenUI(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Searching for Data...')
        self.setGeometry(300, 300, 300, 100)
        layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setText('Searching for Data...')
        layout.addWidget(self.label)
        self.setLayout(layout)
