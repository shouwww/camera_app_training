
""" image tool program
    image tool
"""
import cv2
from logging import INFO, basicConfig, getLogger, NullHandler
import numpy as np
import os
import sys
from PIL import Image, ImageTk


class ImageProcessing:
    """
    image toool class.

    img tool.
    """

    def __init__(self):
        """
        init.

        init.
        """
        # set logger
        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.setLevel(INFO)
        self._logger.propagate = True
        self._logger.info('init img tool')
        # cascade init
        face_cascade_path = 'haarcascades/haarcascade_frontalface_default.xml'
        eye_cascade_path = 'haarcascades/haarcascade_eye.xml'
        self.face_cascade = cv2.CascadeClassifier(face_cascade_path)
        self.eye_cascade = cv2.CascadeClassifier(eye_cascade_path)

        # Init image process parameters
        self.threshold1 = 100
        self.threshold2 = 100
        self.ksize = (3, 3)
        self.sigmaX = 1.3
        self.area_min = 2
        self.area_len_min = 4

        size = (512, 512)
        self.black_img = np.zeros(size, np.uint8)
    # End def

    def set_threshold(self,th1=-1,th2=-1):
        if th1 > -1:
            self.threshold1 = th1
        if th2 > -1:
            self.threshold2 = th2
    # Ebd def

    def detect_face(self, img):
        """
        Detect face method.

        detect face
        """
        self.rate_w = 1.3
        self.rate_h = 1.3
        return_flg = False
        face = self.black_img
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        for x, y, w, h in faces:
            x = int(x - (self.rate_w - 1.0) * 0.5 * w)
            w = int(h * self.rate_w)
            y = int(y - (self.rate_h - 1.0) * 0.5 * w)
            h = int(h * self.rate_h)
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
            face = img[y: y + h, x: x + w]
            face_gray = gray[y: y + h, x: x + w]
            eyes = self.eye_cascade.detectMultiScale(face_gray)
            if len(eyes) >= 2:
                return_flg = True
                break
            # End if
        # End for
        return return_flg, face
    # End def

    def output_line_drawing(self, img):
        """
        Output line drawing.

        data.
        """
        # _img = cv2.bilateralFilter(img, 75, 100, 100)
        _img = cv2.fastNlMeansDenoisingColored(img, None, h=10, hColor=10, templateWindowSize=7, searchWindowSize=21)
        gray_img = _img
        # img_gaus = cv2.GaussianBlur(gray_img, ksize=self.ksize, sigmaX=self.sigmaX)
        img_canny = cv2.Canny(_img, threshold1=self.threshold1, threshold2=self.threshold2)
        contours, hierarchy = cv2.findContours(img_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        data_lines = []
        img_white = np.ones(img_canny.shape, np.uint8) * 255
        for i, data in enumerate(contours):
            data_xy = []
            area = cv2.contourArea(data)
            # Remove noise with small area
            # Remove noise with short line
            if (area < self.area_min) or (len(data) < self.area_len_min):
                pass
                # print(f'pass , i={i} , area={area}, points={len(data)}')  # in debug
            else:
                # print(f'==draw , i={i} , area={area}, points={len(data)}')
                start_point = [0, 0]
                end_point = [0, 0]
                for point in data:
                    data_xy.append([point[0][0], point[0][1]])
                    end_point = [point[0][0], point[0][1]]
                    if start_point == [0, 0]:
                        pass
                    else:
                        img_white = cv2.line(img_white, (start_point[0], start_point[1]), (end_point[0], end_point[1]), (0, 0, 255), 1)
                    # End if
                    start_point = end_point
                # End for
                data_lines.append(data_xy)
            # End if
        # End for
        ret_img = cv2.cvtColor(img_white, cv2.COLOR_GRAY2RGBA)
        return ret_img, contours, data_lines
    # End def

    def resize_tool(self, img, w, h):
        """
        Resize func.

        aaa
        """
        rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        re_img = self._resize(rgb_frame, w, h)
        photo = ImageTk.PhotoImage(image=Image.fromarray(re_img))
        return photo

    def _resize(self, img, width, height):
        """
        Resize func.

        Fix the aspect ratio and resize the image to fit the specified size.
        """
        h, w = img.shape[:2]
        aspect = w / h
        if width / height >= aspect:
            nh = height
            nw = int(nh * aspect)
        else:
            nw = width
            nh = int(nw / aspect)
        dst = cv2.resize(img, [nw, nh])
        return dst
    # End def

# End class


def main():
    """
    try.

    main.
    """
    logger = getLogger(__name__)
    os.makedirs(os.path.join(os.path.dirname(sys.argv[0]), "log"), exist_ok=True)
    basicConfig(level=INFO, filename=os.path.join(os.path.dirname(sys.argv[0]), "log", "imgtoollog.log"), format="%(asctime)s:%(levelname)s:%(message)s ")
    logger.info('img tool rogs')


if __name__ == "__main__":
    main()
