import os, sys
import cv2
import numpy as np
from PIL import Image, ImageTk
from logging import INFO, basicConfig, getLogger
logger = getLogger(__name__)


class CameraTmp():
    def __init__(self):
        self.is_connected = False

    def connect_start(self):
        self.cap = cv2.VideoCapture(0)
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.is_connected = True
        print(self.width, self.height)
    # End def

    def test_func(self):
        while True:
            ret, frame = self.cap.read()
            print(ret)
            cv2.imshow('camera', frame)
            key = cv2.waitKey(10)
            if key == 27:
                break
            # End if
        # End while
    # End def

    def change_img(self, img, w, h):
        rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        re_img = self.resize(rgb_frame, w, h)
        photo = ImageTk.PhotoImage(image=Image.fromarray(re_img))
        return photo
    # End def

    def get_img(self, w, h):
        while True:
            ret, frame = self.cap.read()
            if ret:
                break
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        re_img = self.resize(rgb_frame, w, h)
        photo = ImageTk.PhotoImage(image=Image.fromarray(re_img))
        # pil_img = self.cv2pil(frame)
        # pil_img.show()
        # im_re = pil_img.resize(size=(100, 100))
        return frame, photo
    # End def

    def cv2pil(self, image):
        ''' OpenCV型 -> PIL型 '''
        new_image = image.copy()
        if new_image.ndim == 2:  # モノクロ
            pass
        elif new_image.shape[2] == 3:  # カラー
            new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
        elif new_image.shape[2] == 4:  # 透過
            new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
        new_image = Image.fromarray(new_image)
        return new_image
    # End def

    def resize(self, img, base_w, base_h):
        base_ratio = base_w / base_h   # リサイズ画像サイズ縦横比
        img_h, img_w = img.shape[:2]   # 画像サイズ
        img_ratio = img_w / img_h      # 画像サイズ縦横比

        white_img = np.zeros((base_h, base_w, 3), np.uint8)  # 白塗り画像のベース作成
        white_img[:, :] = [255, 255, 255]                     # 白塗り

        # 画像リサイズ, 白塗りにオーバーレイ
        if img_ratio > base_ratio:
            h = int(base_w / img_ratio)             # 横から縦を計算
            w = base_w                              # 横を合わせる
            resize_img = cv2.resize(img, (w, h))    # リサイズ
        else:
            h = base_h                              # 縦を合わせる
            w = int(base_h * img_ratio)             # 縦から横を計算
            resize_img = cv2.resize(img, (w, h))    # リサイズ

        white_img[int(base_h / 2 - h / 2):int(base_h / 2 + h / 2), int(base_w / 2 - w / 2):int(base_w / 2 + w / 2)] = resize_img    # オーバーレイ
        resize_img = white_img  # 上書き

        return resize_img

    def __del__(self):
        self.cap.release()
        self.is_connected = False
        cv2.destroyAllWindows()
    # End def
# End class


def main():
    os.makedirs(os.path.join(os.path.dirname(sys.argv[0]), "log"), exist_ok=True)
    basicConfig(level=INFO, filename=os.path.join(os.path.dirname(sys.argv[0]), "log", "cameralog.log"), format="%(asctime)s:%(levelname)s:%(message)s ")

    cam = CameraTmp()
    cam.connect_start()
    img = cam.get_img()
    print(type(img))
# End def


if __name__ == "__main__":
    main()
