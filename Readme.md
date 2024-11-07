# 파노라마 영상 제작 및 스터커 추가 프로그램

## Project 설명
- 파노라마 영상을 제작하거나, 제작한 이미지 혹은, 자신이 갖고 있는 이미지에 스티커 사진을 추가할 수 있는 프로그램
- 파노라마 영상을 제작 후 자신이 원하는 스티커 이미지를 가져와 추가하거나 원래 갖고 있던 이미지를 불러와 자신이 원하는 스티커 이미지를 추가하여 수정할 수 있습니다. 

## Data
- 제작시 사용한 이미지는 제작자의 github에 존재합니다.(clone시 같이 받아집니다.)

## Folder 구조
```
app1/
├── project.toml
├── requirements.txt
├── src/
│   ├── picture_sticker.py
├── picture
│   ├── dog.jpg
│   ├── sticker.png
│   ├── sticker_sample.png    
│   └── icn.png
└── README.md
```

## Environment
- python venv

## Code 
0. 가상환경이 없는 경우 다음 명령어로 가상환경 생성

```
python3 -m venv <가상환경 이름> 
```
⬇️ e.g.
```
python -m venv vision_agent 
```

1. 가상환경 활성화 및 필요한 라이브러리 설치
```
window - .\<가상환경 이름>\Scripts\activate
macOS/Linux - source <가상환경 이름>\Scripts\activate

pip install -r .\requirements.txt
```
(오류가 발생한다면 필요한 라이브러리 직접 설치)
```
ERROR: Ignored the following versions that require a different python version: 0.28.0 Requires-Python >=3.7, <3.11; 1.21.2 Requires-Python >=3.7,<3.11; 1.21.3 Requires-Python >=3.7,<3.11; 1.21.4 Requires-Python >=3.7,<3.11; 1.21.5 Requires-Python >=3.7,<3.11; 1.21.6 Requires-Python >=3.7,<3.11
```
라이브러리 설치 명령어
```
pip install <라이브러리 이름>
```
⬇️ e.g.
```
ModuleNotFoundError: No module named 'cv2'
--> pip install opencv-python
```

2. 코드 실행 
```
python picture_sticker.py
```
