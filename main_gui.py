import tkinter
import tkinter.messagebox
import customtkinter
from pycamera import CameraTmp

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")
        self.grid_columnconfigure([0, 1], weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.cam = CameraTmp()
        self.after_id = 0

        # create frame
        self.main_frame = customtkinter.CTkFrame(master=self, width=840, corner_radius=0)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.set_up_header(self.main_frame, header_name="お絵かきアプリ")
        self.sub_frame = customtkinter.CTkFrame(master=self, width=840, corner_radius=0)
        self.sub_frame.grid(row=2, column=0, sticky="ew")
        self.set_up_setting(self.sub_frame)
        self.thumbnail_frame = customtkinter.CTkFrame(self, width=400, corner_radius=0)
        self.thumbnail_frame.grid(row=0, column=1, rowspan=3, sticky="ns")
        test_labeal3 = customtkinter.CTkButton(self.thumbnail_frame, text='thumbnail frame', width=180)
        test_labeal3.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        # main frame
        # view 1 frame in main frame
        self.cam_frame = customtkinter.CTkFrame(master=self)
        self.cam_frame.grid(row=1, column=0, sticky="nsew")
        
        self.view1_frame = customtkinter.CTkFrame(master=self.cam_frame)
        self.view1_frame.pack(fill="both", expand=True, side=customtkinter.LEFT)
        self.view2_frame = customtkinter.CTkFrame(master=self.cam_frame, fg_color='white')
        self.view2_frame.pack(fill="both", expand=True, side=customtkinter.LEFT)
        self.image_label = customtkinter.CTkLabel(self.view1_frame, text="AAAAA")  # display image with a CTkLabel

        # view 2 frame in main frame
        # sub frame , output log , Quit btn, setting slider *2 
        # initial set
    # End def

    def set_up_header(self, master_frame: customtkinter.CTkFrame, header_name):
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
        master_frame.grid_columnconfigure(0, weight=1)
        master_frame.grid_rowconfigure(0, weight=1)
        self.log_tb = customtkinter.CTkTextbox(master_frame, width=450, height=80)
        self.log_tb.grid(row=0, column=0, rowspan=2, padx=5, pady=5, sticky='ew')
        self.slider_threshold_1 = customtkinter.CTkSlider(master_frame, from_=0, to=600, number_of_steps=600, command=self.set_threshold_1)
        self.slider_threshold_1.grid(row=0, column=1, padx=5, pady=5)
        self.slider_threshold_2 = customtkinter.CTkSlider(master_frame, from_=0, to=600, number_of_steps=600, command=self.set_threshold_2)
        self.slider_threshold_2.grid(row=1, column=1, padx=5, pady=5)
        self.txt_threshhold_1 = customtkinter.CTkTextbox(master_frame, width=40, height=2)
        self.txt_threshhold_1.grid(row=0, column=2)
        self.txt_threshhold_2 = customtkinter.CTkTextbox(master_frame, width=40, height=2)
        self.txt_threshhold_2.grid(row=1, column=2)
        self.quit_btn = customtkinter.CTkButton(master_frame, text='Quit', width=20)
        self.quit_btn.grid(row=0, column=3, rowspan=2)

    def start_callback_func(self):
        self.cam.connect_start()
        self.is_running = True
        self.update_func()
        self.start_btn.configure(fg_color='gray')
        self.stop_btn.configure(fg_color='green')
    # End def



    def stop_callback_func(self):
        self.is_running = False
        self.after_cancel(self.after_id)
        self.stop_btn.configure(fg_color='gray')
        self.start_btn.configure(fg_color='green')


    def write_log(self, msg=""):
        numlines = int(self.log_tb.index('end - 1 line').split('.')[0])
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


    def update_func(self):
        # update io state from robot controler interval
        update_interval = 10
        img = self.cam.get_img()
        print(img)
        my_image = customtkinter.CTkImage(dark_image=img)
        self.image_label.configure(image=my_image)

        self.after_id = self.after(update_interval, self.update_func)
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
        numlines = int(self.log_tb.index('end - 1 line').split('.')[0])
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


# End class


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
