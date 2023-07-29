import cv2
from PIL import Image



class TimeIn(customtkinter.CTk):
    ...
    # code for video streaming
    def streaming(self):
        cap = cv2.VideoCapture(0)
        ret, img = cap.read()
        cv2image= cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        ImgTks = ImageTk.PhotoImage(image=img)
        self.camera.imgtk = ImgTks
        self.camera.configure(image=ImgTks)
        self.after(20, self.streaming)


if __name__ == "__main__":
    app = TimeIn()
    app.streaming()
    app.mainloop()