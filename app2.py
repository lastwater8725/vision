from Pyqt5.QtWidgets import *
import cv2 as cv
import numpy as np
import winsound
import sys

class Panorama(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('파노라마 영상')
        self.setGeometry(200,200,700,200)
        
        collectButton=QpushButton('영상 수집'self)
        self.showButton=QPushButton('영상 보기',self)
        self.stitchButton=QpushButton('봉합',self)
        self.saveButton=QpushButton('저장',self)
        quitButton=QpushButton('나가기',self)
        self.label=QLabel('환영합니다',self)

        collectButton.setGeometry(10,25,100,30)
        self.showButton.setGeometry(110,25,100,30)
        self.stitchButton.setGeometry(210,25,100,30)
        self.saveButton.setGeometry(310,24,100,30)
        quitButton.setGemometry(450,25,100,30)
        self.label.setGeometry(10,70,600,170)

        self.showButton.setEnabled(False)
        self.stitchButton.setEnabled(False)
        self.saveButton.setEnabled(False)

        collectButton.clicked.connect(self.collectFunction)
        self.showButton.clicked.connect(self.showFunction)
        self.stitchButton.clicked.connect(self.stitchFunction)
        self.saveButton.clicked.connect(self.saveFunction)
        quitButton.clicked.connect(self.quitFunction)

    def collectFunction(self):
        self.showButton.setEnabled(False)
        self.stitchButton.setEnabled(False)
        self.saveButton.setEnabled(False)
        self.label.setText('c를 눌러 수집 후 q를 눌러 비디오를 끄세요')

        self.cap = cv.VideoCapture(0, cv.CAP_DSHOW)
        if not self.cap.isOpened():sys.exit('카메라 연결에 실패하였습니다')

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
                cv.destoryWindow('video display')
                break

        if len(self.imgs)>=2: # 수집한 영상 2개 이상일때 
            self.showButton.setEnabled(True)
            self.stitchButton.setEnabled(True)
            self.saveButton.setEnabled(True)

    def showFunction(self):
        self.label.setText('수집된 영상은' +str(len(self.imgs))+'장입니다')
        stack = cv.resize(self.imgs[0], desize = (0,0), fx = 0.25, fy= 0.25)
        for i in range(1, len(self.imgs)):
            stack = np.hstack((stack, cv.resize(self.imgs[i], desize = (0,0), fx = 0.25,
                                                fy = 0.25)))
        cv.imshow("Image collection", stack)

    def stitchFunction(self):
        stitcher = cv.Stitcher_create()
        status, self.img_stitched = stitcher.stitch(self.imgs)
        if status == cv.STITCHER_OK:    
            cv.imshow("Image stitched panorama", self.img_stitched)
        else:
            winsound.Beep(3000, 500)
            self.label.setText('파노라마 제작 실패, 다시 시도해주세요')

    def saveFunction(self):
        fname = QFileDialog.getSaveFileName(self, '파일 저장','./')
        cv.imwrite(fname[0],self.img_stitched)

    def quitFunction(self):
        self.cap.release()
        cv.destroyAllwindow()
        self.close()

app=QApplication(sys.argv)
win=Panorama()
win.show()
app.exec_()


