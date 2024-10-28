import sys
import winsound

from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel



#nodemon을 써라?

class BeepSound(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("삑 소리 내기", self)
        self.setGeometry(200, 200, 500, 100)

        short_beep_btn = QPushButton("짧게 삑", self)
        long_beep_btn = QPushButton("길게 삑", self)
        quit_btn = QPushButton("나가기", self)
        self.label = QLabel("환영합니다", self)

        short_beep_btn.setGeometry(10, 10, 100, 30)
        long_beep_btn.setGeometry(110, 10, 100, 30)
        quit_btn.setGeometry(210, 10, 100, 30)  
        self.label.setGeometry(10, 40, 500, 70)
        
        short_beep_btn.clicked.connect(self.short_beep)
        quit_btn.clicked.connect(self.quit_fn)

    def short_beep(self):
        self.label.setText("주파수 1000으로 0.5초")
        winsound.Beep(1000, 500)

    def quit_fn(self):
        self.close


if __name__ == "__main__":
    app = QApplication([])
    win = BeepSound()
    win.show()
    app.exec()



# pyqt실행파일 만들기 