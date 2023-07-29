import cv2
from PIL import Image, ImageTk


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
            #繰り返し分から抜けるためのif文
            key =cv2.waitKey(10)
            if key == 27:
                break

    def get_img(self):
        while True:
            ret, frame = self.cap.read()
            if ret:
                break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        pil_img = self.cv2pil(frame)
        # pil_img.show()
        im_re = pil_img.resize(size=(100, 100))
        return photo
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

    def __del__(self):
        self.cap.release()
        self.is_connected = False
        cv2.destroyAllWindows()
    # End def
# End class


def main():
    cam = CameraTmp()
    cam.connect_start()
    img = cam.get_img()
    img = cam.test_func()
# End def


if __name__ == "__main__":
    main()
