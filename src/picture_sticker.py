import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QAction 
import cv2 as cv
import numpy as np
import sys

class Panorama(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('파노라마 영상 및 사진 수정')
        self.resize(500,350)
        self.setWindowIcon(QIcon('./picture/icn.png'))
        self.setGeometry(1100, 200, 700, 200)

        collectButton = QPushButton('영상 수집',self)
        self.showButton = QPushButton('영상 보기',self)
        self.stitchButton = QPushButton('봉합',self)
        self.saveButton = QPushButton('저장',self)
        self.pictureButton = QPushButton('사진 불러오기', self)
        self.stickerButton = QPushButton('스티커 추가하기', self)
        self.stickerImageButton = QPushButton('스티커 이미지 불러오기', self)
        quitButton = QPushButton('나가기',self)
        self.label = QLabel("환영합니다. 스티커 사진 제작시 클릭하면 스티커가 추가됩니다", self)
        self.enter = QLabel('파노라마 사진 촬영 및 사진 꾸미기 프로그램입니다.',self)
        self.enter.setStyleSheet("color: red;")

        collectButton.setGeometry(10,25,100,30)
        self.showButton.setGeometry(110,25,100,30)
        self.stitchButton.setGeometry(210,25,100,30)
        self.saveButton.setGeometry(310,25,100,30)
        self.pictureButton.setGeometry(10, 52, 100, 30)
        self.stickerButton.setGeometry(110, 52, 100, 30)
        self.stickerImageButton.setGeometry(210, 52, 140, 30)
        quitButton.setGeometry(450,25,100,30)
        self.label.setGeometry(10,70,600,170)
        self.enter.setGeometry(10,90,600,170)

        self.showButton.setEnabled(False)
        self.stitchButton.setEnabled(False)
        self.saveButton.setEnabled(False)
        self.stickerButton.setEnabled(False)

        collectButton.clicked.connect(self.collectFunction)
        self.showButton.clicked.connect(self.showFunction)
        self.stitchButton.clicked.connect(self.stitchFunction)
        self.saveButton.clicked.connect(self.saveFunction)
        self.pictureButton.clicked.connect(self.pictureFunction)
        self.stickerButton.clicked.connect(self.addSticker)
        quitButton.clicked.connect(self.quitFunction)
        self.stickerImageButton.clicked.connect(self.loadStickerImage)

        self.statusBar().showMessage('준비됨')     

        self.image = None
        self.sticker = None
        self.sticker_resized = None
        self.click_position = None   

    def pictureFunction(self):
        filename, _ = QFileDialog.getOpenFileName(self, '이미지 파일 선택', '', '이미지 파일 (*.jpg *.jpeg *.png *.bmp)')
        if filename:
            self.label.setText(f'선택된 파일: {filename}')
            self.image = cv.imread(filename)
            self.stickerButton.setEnabled(True)
        else:
            self.label.setText('파일을 선택하지 않았습니다.')

    def loadStickerImage(self):
        sticker_filename, _ = QFileDialog.getOpenFileName(self, '스티커 이미지 선택', '', '이미지 파일 (*.jpg *.jpeg *.png *.bmp)')
        if sticker_filename:
            self.sticker = cv.imread(sticker_filename, cv.IMREAD_UNCHANGED)
            self.label.setText(f'스티커 이미지 선택됨: {sticker_filename}')
            if self.image is not None:
                self.sticker_resized = cv.resize(self.sticker, (self.image.shape[1] // 4, self.image.shape[0] // 4))
        else:
            self.label.setText('스티커 이미지가 선택되지 않았습니다.')

    def addSticker(self):
        if self.image is None or self.sticker_resized is None:
            self.label.setText('원본 이미지와 스티커 이미지가 모두 필요합니다.')
            return
        self.label.setText('왼쪽마우스를 클릭하여 추가 후 q를 눌러 사진을 확인하세요')
        key = cv.waitKey(1)
        if key == ord('q'):
            cv.destroyWindow('video display')
        cv.imshow("원본 이미지", self.image)
        cv.setMouseCallback("원본 이미지", self.mouseCallback)
        cv.waitKey(0)
        cv.destroyAllWindows()

        if self.click_position:
            x_offset, y_offset = self.click_position
            h, w = self.sticker_resized.shape[:2]
            if y_offset + h > self.image.shape[0]:
                h = self.image.shape[0] - y_offset
            if x_offset + w > self.image.shape[1]:
                w = self.image.shape[1] - x_offset

            if self.sticker_resized.shape[2] == 4:
                alpha_channel = self.sticker_resized[:,:,3:] / 255.0
                for c in range(3):
                    self.image[y_offset:y_offset+h, x_offset:x_offset+w, c] = \
                        self.sticker_resized[:h,:w,:3] * alpha_channel[:h,:w] + \
                        self.image[y_offset:y_offset+h, x_offset:x_offset+w, c] * (1.0 - alpha_channel[:h,:w])
            else:
                self.image[y_offset:y_offset+h, x_offset:x_offset+w] = self.sticker_resized[:h,:w]
            cv.imshow("스티커 추가된 이미지", self.image)

        if len(self.image)>=1:
            self.saveButton.setEnabled(True)

    def mouseCallback(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            self.click_position = (x, y)
            self.label.setText(f'클릭한 위치: ({x}, {y})')
            key = cv.waitKey(1)

    def collectFunction(self):
        self.showButton.setEnabled(False)
        self.stitchButton.setEnabled(False)
        self.saveButton.setEnabled(False)
        self.label.setText('c를 눌러 수집 후 q를 눌러 비디오를 끄세요')

        self.cap = cv.VideoCapture(0, cv.CAP_DSHOW)
        if not self.cap.isOpened(): sys.exit('카메라 연결에 실패하였습니다')

        self.imgs=[]
        while True:
            ret,frame=self.cap.read()
            if not ret: break
            cv.imshow('video display', frame)
            key = cv.waitKey(1)
            if key == ord('c'):
                self.imgs.append(frame)
            elif key == ord('q'):
                self.cap.release()
                cv.destroyWindow('video display')
                break

        if len(self.imgs)>=2:
            self.showButton.setEnabled(True)
            self.stitchButton.setEnabled(True)
            self.saveButton.setEnabled(True)

    def showFunction(self):
        self.label.setText(f'수집된 영상은 {len(self.imgs)} 장입니다.')
        stack = cv.resize(self.imgs[0], dsize = (0,0), fx = 0.25, fy= 0.25)
        for i in range(1, len(self.imgs)):
            stack = np.hstack((stack, cv.resize(self.imgs[i], dsize = (0,0), fx = 0.25,
                                                fy = 0.25)))
        cv.imshow("Image collection", stack)

    def stitchFunction(self):
        stitcher = cv.Stitcher_create()
        status, self.img_stitched = stitcher.stitch(self.imgs)
        if status == cv.STITCHER_OK:
            cv.imshow("Image stitched", self.img_stitched)
            self.saveButton.setEnabled(True)
        else:
            print("이미지 결합 실패")

    def saveFunction(self):
        filename, _ = QFileDialog.getSaveFileName(self, '파일 저장', '', '이미지 파일 (*.jpg *.jpeg *.png *.bmp)')
        if filename:
            if hasattr(self, 'img_stitched') and self.img_stitched is not None:
                cv.imwrite(filename, self.img_stitched)
                self.label.setText(f'{filename}로 저장되었습니다.')
            elif self.image is not None:
                cv.imwrite(filename, self.image)
                self.label.setText(f'{filename}로 저장되었습니다.')
            else:
                self.label.setText('저장할 이미지가 없습니다.')

    def quitFunction(self):
        sys.exit()

app = QApplication(sys.argv)
window = Panorama()
window.show()
app.exec()
