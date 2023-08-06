import cv2


def hconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    h_min = min(im.shape[0] for im in im_list)
    im_list_resize = [cv2.resize(im, (int(im.shape[1] * h_min / im.shape[0]), h_min), interpolation=interpolation)
                      for im in im_list]
    return cv2.hconcat(im_list_resize)

def cascade_test():
    face_cascade_path = 'haarcascades/haarcascade_frontalface_default.xml'
    eye_cascade_path = 'haarcascades/haarcascade_eye.xml'
    face_cascade = cv2.CascadeClassifier(face_cascade_path)
    eye_cascade = cv2.CascadeClassifier(eye_cascade_path)
    cap = cv2.VideoCapture(0)
    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        print('face')
        if len(faces) == 1:
            for x, y, w, h in faces:
                face = img[y: y + h, x: x + w]
                # face = cv2.bilateralFilter(face, 75, 100, 100)
                face = cv2.fastNlMeansDenoisingColored(face,None,h=10,hColor=10,templateWindowSize=7,searchWindowSize=21)
                face_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                eyes = eye_cascade.detectMultiScale(face_gray)
                print(f'eyes : {len(eyes)}')
                th1 = 50
                th2 = 100
                #face_gaus = cv2.GaussianBlur(face_gray, ksize=(3, 3), sigmaX=1.3)
                face_gaus = face_gray
                face_canny = cv2.Canny(face_gaus, threshold1=th1, threshold2=th2)
                im_h = hconcat_resize_min([face_gray, face_gaus, face_canny])
                contours, hierarchy = cv2.findContours(face_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                output = cv2.drawContours(face, contours, -1, (0, 255, 0), 3)
            cv2.imshow('face color ', im_h)
            cv2.imshow('draw_output', output)
            cv2.moveWindow('draw_output', 100, 200)
        # End if
        key = cv2.waitKey(10)
        if key == 27:  # ESCキーで終了
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    cascade_test()
