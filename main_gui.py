import os, sys, glob, datetime
import tkinter
import tkinter.messagebox
import customtkinter
import cv2
from logging import INFO, basicConfig, getLogger
from pycamera import CameraTmp
from pyImageProcessing import ImageProcessing

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
logger = getLogger(__name__)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CustomTkinter window")
        # self.state('zoomed')
        # self.geometry(f"{1100}x{580}")
        # self.attributes('-fullscreen', True)
        self.grid_columnconfigure([0, 1], weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.cam = CameraTmp()
        self.img_tool = ImageProcessing()
        self.after_id = 0

        self.img_width = 320
        self.img_height = 240

        self.mode = 'stop'
        self.base_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
        self.img_dir = os.path.join(self.base_dir, 'images')
        os.makedirs(self.img_dir, exist_ok=True)
        self.rowimg_dir = ''
        self.faceimg_dir = ''
        self.thumbnail_imgs = []
        self.select_thumbnail = 0

        # create frame
        self.main_frame = customtkinter.CTkFrame(master=self, width=2 * self.img_width / 3, corner_radius=0)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.set_up_header(self.main_frame, header_name="お絵かきアプリ")
        self.sub_frame = customtkinter.CTkFrame(master=self, width=2 * self.img_width / 3, corner_radius=0)
        self.sub_frame.grid(row=2, column=0, sticky="ew")
        self.set_up_setting(self.sub_frame)
        self.thumbnail_frame = customtkinter.CTkFrame(self, width=self.img_width / 3, corner_radius=0)
        self.thumbnail_frame.grid(row=0, column=1, rowspan=3, padx=(0, 20), pady=(20, 20), sticky="nsew")
        self.thumbnail_frame.grid_columnconfigure([0, 1, 2], weight=1)
        self.thumbnail_frame.grid_rowconfigure([0, 1, 2, 3, 4], weight=1)
        # test_labeal3 = customtkinter.CTkButton(self.thumbnail_frame, text='thumbnail frame', width=180)
        # test_labeal3.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        # main frame
        # view 1 frame in main frame
        self.cam_frame = customtkinter.CTkFrame(master=self)
        self.cam_frame.grid(row=1, column=0, sticky="nsew")
        # view1 is left frame . used usb camera image view org images
        self.view1_frame = customtkinter.CTkFrame(master=self.cam_frame)
        self.view1_frame.pack(fill="both", expand=True, side=customtkinter.LEFT)
        self.view1_frame.grid_columnconfigure([0, 1], weight=1)
        self.view1_frame.grid_rowconfigure(0, weight=1)
        # view2 is right frame . used edited images
        self.view2_frame = customtkinter.CTkFrame(master=self.cam_frame)
        self.view2_frame.pack(fill="both", expand=True, side=customtkinter.LEFT)
        self.view2_frame.grid_columnconfigure([0, 1], weight=1)
        self.view2_frame.grid_rowconfigure(0, weight=1)
        # self.image_label = customtkinter.CTkLabel(self.view1_frame, text="AAAAA")  # display image with a CTkLabel
        self.img1_canva = tkinter.Canvas(self.view1_frame)
        self.img1_canva.configure(width=self.img_width, height=self.img_height)
        self.img1_canva.grid(column=0, row=0, columnspan=2, sticky="nsew")
        self.back1_btn = customtkinter.CTkButton(self.view1_frame, text='<<', width=20)
        self.forward1_btn = customtkinter.CTkButton(self.view1_frame, text='>>', width=20)
        self.back1_btn.grid(column=0, row=1, sticky='ew')
        self.forward1_btn.grid(column=1, row=1, sticky='ew')
        # view 2 frame in main frame
        self.img2_canva = tkinter.Canvas(self.view2_frame)
        self.img2_canva.configure(width=self.img_width, height=self.img_height)
        self.img2_canva.grid(column=0, row=0, columnspan=2, sticky="nsew")
        self.back2_btn = customtkinter.CTkButton(self.view2_frame, text='<<', width=20, command=lambda: self.view2_btn_callback(-1))
        self.forward2_btn = customtkinter.CTkButton(self.view2_frame, text='>>', width=20, command=lambda: self.view2_btn_callback(1))
        self.back2_btn.grid(column=0, row=1, sticky='ew')
        self.forward2_btn.grid(column=1, row=1, sticky='ew')
        # thumbnail_s
        self.thumbnail_canvasses = []
        for i in range(15):
            col = i % 3
            row = i // 3
            self.thumbnail_canvasses.append(tkinter.Canvas(self.thumbnail_frame, width=5, height=10, relief='flat', bg='white', bd=1))
            self.thumbnail_canvasses[-1].grid(column=col, row=row, padx=1, pady=1, sticky=('nsew'))
        # initial set
        self.main_frame.bind("<Configure>", self.resize)
        self.after(0, lambda: self.wm_state('zoomed'))
    # End def

    def set_up_header(self, master_frame: customtkinter.CTkFrame, header_name):
        """
        set top label area widjet
        """
        self.main_top_label = customtkinter.CTkLabel(master_frame, text=header_name)
        self.main_top_label.grid(row=0, column=0, padx=5, pady=5)
        self.main_cam_label = customtkinter.CTkLabel(master_frame, text='CameraNo')
        self.main_cam_label.grid(row=0, column=1, padx=5, pady=5)
        self.cam_id_comb = customtkinter.CTkComboBox(master_frame, values=['0', '1', '2', '3', '4', '5'])
        self.cam_id_comb.grid(row=1, column=1, padx=5, pady=5)
        self.start_btn = customtkinter.CTkButton(master_frame, text='start', fg_color='green', hover=False, command=self.start_callback_func)
        self.start_btn.grid(row=0, column=2, padx=5, pady=5)
        self.stop_btn = customtkinter.CTkButton(master_frame, text='stop', fg_color='gray', hover=False, command=self.stop_callback_func)
        self.stop_btn.grid(row=0, column=3, padx=5, pady=5)
        self.setting_btn = customtkinter.CTkButton(master_frame, text='Setting')
        self.setting_btn.grid(row=1, column=2, padx=5, pady=5)
        self.handwrite_btn = customtkinter.CTkButton(master_frame, text='handwrite')
        self.handwrite_btn.grid(row=1, column=3, padx=5, pady=5)

    def set_up_setting(self, master_frame: customtkinter.CTkFrame):
        """
        set bottom label area widjet
        """
        master_frame.grid_columnconfigure(0, weight=1)
        master_frame.grid_rowconfigure(0, weight=1)
        self.log_tb = customtkinter.CTkTextbox(master_frame, width=300, height=80)
        self.log_tb.grid(row=0, column=0, rowspan=2, padx=5, pady=5, sticky='ew')
        self.slider_threshold_1 = customtkinter.CTkSlider(master_frame, width=400, from_=0, to=600, number_of_steps=600, command=self.set_threshold_1)
        self.slider_threshold_1.grid(row=0, column=1, padx=5, pady=5)
        self.slider_threshold_2 = customtkinter.CTkSlider(master_frame, width=400, from_=0, to=600, number_of_steps=600, command=self.set_threshold_2)
        self.slider_threshold_2.grid(row=1, column=1, padx=5, pady=5)
        self.txt_threshhold_1 = customtkinter.CTkTextbox(master_frame, width=40, height=2)
        self.txt_threshhold_1.grid(row=0, column=2)
        self.txt_threshhold_2 = customtkinter.CTkTextbox(master_frame, width=40, height=2)
        self.txt_threshhold_2.grid(row=1, column=2)
        self.quit_btn = customtkinter.CTkButton(master_frame, text='Quit', width=20)
        self.quit_btn.grid(row=0, column=3, rowspan=2)
        self.slider_threshold_1.set(100)
        self.slider_threshold_2.set(200)

    def view2_btn_callback(self, type_btn=0):
        """
        preview image select
        """
        files = glob.glob(self.rowimg_dir + '/*.png')
        face_files = glob.glob(self.faceimg_dir + '/*.png')
        if len(files) > 0:
            self.select_thumbnail = self.select_thumbnail + type_btn
            if self.select_thumbnail > 14:
                self.select_thumbnail = 14
            elif self.select_thumbnail < 0:
                self.select_thumbnail = 0
            elif self.select_thumbnail > len(files) - 1:
                self.select_thumbnail = len(files) - 1
            # End if
            files.sort()
            face_files.sort()
            self.write_log(str(self.select_thumbnail))
            im = cv2.imread(files[self.select_thumbnail])
            face = cv2.imread(face_files[self.select_thumbnail])
            face_line, contours, data_lines = self.img_tool.output_line_drawing(face)
            canvas_h = self.img2_canva.winfo_height()
            canvas_w = self.img2_canva.winfo_width()
            self.im2 = self.cam.change_img(face_line, canvas_w, canvas_h)
            self.re_face = self.img_tool.resize_tool(face, w=canvas_w, h=canvas_h)
            self.img1_canva.create_image(0, 0, image=self.re_face, anchor='nw')
            self.img2_canva.create_image(0, 0, image=self.im2, anchor='nw')
        # End if
    # End def

    def start_callback_func(self):
        """
        start recording image btn
        """
        if len(self.thumbnail_imgs) > 0:
            self.thumbnail_imgs = []
        now = datetime.datetime.now()
        self.img_dir = os.path.join(self.base_dir, 'images', now.strftime('%Y%m%d_%H%M%S_%f'))
        os.makedirs(self.img_dir, exist_ok=True)
        self.rowimg_dir = os.path.join(self.img_dir, 'row_imgs')
        self.faceimg_dir = os.path.join(self.img_dir, 'face_imgs')
        os.makedirs(self.rowimg_dir, exist_ok=True)
        os.makedirs(self.faceimg_dir, exist_ok=True)
        self.cam.connect_start()
        self.is_running = True
        self.update_func()
        self.start_btn.configure(fg_color='gray')
        self.stop_btn.configure(fg_color='green')
    # End def

    def stop_callback_func(self):
        """
        stop recording image btn
        """
        self.is_running = False
        self.after_cancel(self.after_id)
        self.stop_btn.configure(fg_color='gray')
        self.start_btn.configure(fg_color='green')
    # End def

    def write_log(self, msg=""):
        """
        write log viewer string
        """
        # numlines = int(self.log_tb.index('end - 1 line').split('.')[0])
        self.log_tb['state'] = 'normal'
        if self.log_tb.index('end-1c') != '1.0':
            self.log_tb.insert('end', '\n')
        self.log_tb.insert('end', msg)
        self.log_tb.see("end")
        self.log_tb['state'] = 'disabled'
    # End def

    def set_threshold_1(self, value):
        self.txt_threshhold_1['state'] = 'normal'
        self.txt_threshhold_1.delete("0.0", "end")
        self.txt_threshhold_1.insert("end", str(int(value)))
        self.txt_threshhold_1['state'] = 'disabled'
        self.value_threshhold_1 = int(value)
        self.img_tool.set_threshold(th1=value)
        self.view2_btn_callback(type_btn=0)
    # End def

    def set_threshold_2(self, value):
        self.txt_threshhold_2['state'] = 'normal'
        self.txt_threshhold_2.delete("0.0", "end")
        self.txt_threshhold_2.insert("end", str(int(value)))
        self.txt_threshhold_2['state'] = 'disabled'
        self.value_threshhold_2 = int(value)
        self.img_tool.set_threshold(th2=value)
        self.view2_btn_callback(type_btn=0)
    # End def

    def resize(self, event):
        width = self.winfo_width()
        heigh = self.winfo_height()
        print(width, heigh)
    # End def

    def update_func(self):
        # update io state from robot controler interval
        update_interval = 100
        canvas_h = self.img1_canva.winfo_height()
        canvas_w = self.img1_canva.winfo_width()
        thumbnail_h = self.thumbnail_canvasses[0].winfo_height()
        thumbnail_w = self.thumbnail_canvasses[0].winfo_width()
        self.frame, self.img = self.cam.get_img(w=canvas_w, h=canvas_h)
        face_flg, self.face_frame = self.img_tool.detect_face(self.frame)
        self.re_face = self.img_tool.resize_tool(self.face_frame, w=canvas_w, h=canvas_h)
        now = datetime.datetime.now()
        row_img_path = os.path.join(self.rowimg_dir, now.strftime('%Y%m%d_%H%M%S_%f') + '.png')
        face_img_path = os.path.join(self.faceimg_dir, now.strftime('%Y%m%d_%H%M%S_%f') + '.png')
        self.img1_canva.create_image(0, 0, image=self.img, anchor=tkinter.NW)
        if face_flg:
            cv2.imwrite(row_img_path, self.frame)
            cv2.imwrite(face_img_path, self.face_frame)
            self.img2_canva.create_image(0, 0, image=self.re_face, anchor=tkinter.NW)
            self.thumbnail_img = self.img_tool.resize_tool(self.face_frame, thumbnail_w, thumbnail_h)
            img_files = glob.glob(self.rowimg_dir + '/*.png')
            print(len(img_files) - 1)
            self.thumbnail_imgs.append(self.thumbnail_img)
            for i in range(len(self.thumbnail_imgs)):
                self.thumbnail_canvasses[i].create_image(0, 0, image=self.thumbnail_imgs[i], anchor=tkinter.NW)
        if len(self.thumbnail_imgs) >= 15:
            self.stop_callback_func()
        else:
            self.after_id = self.after(update_interval, self.update_func)
        # End if
    # End def
# End class


class HeaderFrame(customtkinter.CTkFrame):
    def __init__(self, *args, header_name="AppName", cv_class=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        # Form setup
        self.setup_form()
        self.cam = cv_class
        self.is_running = False
    # End def init

    def setup_form(self):
        self.main_top_label = customtkinter.CTkLabel(self, text=self.header_name)
        self.main_top_label.grid(row=0, column=0, padx=5, pady=5)
        self.main_cam_label = customtkinter.CTkLabel(self, text='CameraNo')
        self.main_cam_label.grid(row=0, column=1, padx=5, pady=5)
        self.cam_id_comb = customtkinter.CTkComboBox(self, values=['0', '1', '2', '3', '4', '5'])
        self.cam_id_comb.grid(row=1, column=1, padx=5, pady=5)
        self.start_btn = customtkinter.CTkButton(self, text='start', fg_color='green', command=self.start_callback_func)
        self.start_btn.grid(row=0, column=2, padx=5, pady=5)
        self.stop_btn = customtkinter.CTkButton(self, text='stop', fg_color='gray', command=self.start_callback_func)
        self.stop_btn.grid(row=0, column=3, padx=5, pady=5)
        self.setting_btn = customtkinter.CTkButton(self, text='Setting')
        self.setting_btn.grid(row=1, column=2, padx=5, pady=5)
        self.handwrite_btn = customtkinter.CTkButton(self, text='handwrite')
        self.handwrite_btn.grid(row=1, column=3, padx=5, pady=5)

    def start_callback_func(self):
        self.cam.connect_start()
        self.is_running = True
    # End def

    def stop_callback_func(self):
        self.is_running = False
    # End def
# End class


class SettingFrame(customtkinter.CTkFrame):
    def __init__(self, *args, header_name="AppName", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        # Form setup
        self.setup_form()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.value_threshhold_1 = 0
        self.value_threshhold_2 = 0
    # End def init

    def setup_form(self):
        self.log_tb = customtkinter.CTkTextbox(self, width=450, height=80)
        self.log_tb.grid(row=0, column=0, rowspan=2, padx=5, pady=5, sticky='ew')
        self.slider_threshold_1 = customtkinter.CTkSlider(self, from_=0, to=600, number_of_steps=600, command=self.set_threshold_1)
        self.slider_threshold_1.grid(row=0, column=1, padx=5, pady=5)
        self.slider_threshold_2 = customtkinter.CTkSlider(self, from_=0, to=600, number_of_steps=600, command=self.set_threshold_2)
        self.slider_threshold_2.grid(row=1, column=1, padx=5, pady=5)
        self.txt_threshhold_1 = customtkinter.CTkTextbox(self, width=40, height=2)
        self.txt_threshhold_1.grid(row=0, column=2)
        self.txt_threshhold_2 = customtkinter.CTkTextbox(self, width=40, height=2)
        self.txt_threshhold_2.grid(row=1, column=2)

        self.quit_btn = customtkinter.CTkButton(self, text='Quit', width=20)
        self.quit_btn.grid(row=0, column=3, rowspan=2)

    def write_log(self, msg=""):
        # numlines = int(self.log_tb.index('end - 1 line').split('.')[0])
        self.log_tb['state'] = 'normal'
        if self.log_tb.index('end-1c') != '1.0':
            self.log_tb.insert('end', '\n')
        self.log_tb.insert('end', msg)
        self.log_tb.see("end")
        self.log_tb['state'] = 'disabled'
    # End def

    def set_threshold_1(self, value):
        self.txt_threshhold_1['state'] = 'normal'
        self.txt_threshhold_1.delete("0.0", "end")
        self.txt_threshhold_1.insert("end", str(int(value)))
        self.txt_threshhold_1['state'] = 'disabled'
        self.value_threshhold_1 = int(value)
    # End def

    def set_threshold_2(self, value):
        self.txt_threshhold_2['state'] = 'normal'
        self.txt_threshhold_2.delete("0.0", "end")
        self.txt_threshhold_2.insert("end", str(int(value)))
        self.txt_threshhold_2['state'] = 'disabled'
        self.value_threshhold_2 = int(value)
    # End def

    def slider_event(self, value):
        self.write_log(str(value))
    # End def
# End class


def main():
    os.makedirs(os.path.join(os.path.dirname(sys.argv[0]), "log"), exist_ok=True)
    basicConfig(level=INFO, filename=os.path.join(os.path.dirname(sys.argv[0]), "log", "mainlog.log"), format="%(asctime)s:%(levelname)s:%(message)s ")
    logger.info('rob lib rogs')
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
