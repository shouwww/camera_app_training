import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # create frame
        self.main_frame = customtkinter.CTkFrame(self, width=840, corner_radius=0)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.sub_frame = customtkinter.CTkFrame(self, width=840, corner_radius=0)
        self.sub_frame.grid(row=1, column=0, sticky="ew")
        self.thumbnail_frame = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        self.thumbnail_frame.grid(row=0, column=1, rowspan=2, sticky="ns")
        test_labeal3 = customtkinter.CTkButton(self.thumbnail_frame, text='thumbnail frame', width=180)
        test_labeal3.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # main frame
        self.main_top_label = customtkinter.CTkLabel(self.main_frame, text='お絵かきアプリ')
        self.main_top_label.grid(row=0, column=0, padx=5, pady=5)
        self.main_cam_label = customtkinter.CTkLabel(self.main_frame, text='CameraNo')
        self.main_cam_label.grid(row=0, column=1, padx=5, pady=5)
        self.cam_id_comb = customtkinter.CTkComboBox(self.main_frame, values=['0', '1', '2', '3', '4', '5'])
        self.cam_id_comb.grid(row=1, column=1, padx=5, pady=5)
        self.start_btn = customtkinter.CTkButton(self.main_frame, text='start')
        self.start_btn.grid(row=0, column=2, padx=5, pady=5)
        self.stop_btn = customtkinter.CTkButton(self.main_frame, text='stop')
        self.stop_btn.grid(row=0, column=3, padx=5, pady=5)
        self.setting_btn = customtkinter.CTkButton(self.main_frame, text='Setting')
        self.setting_btn.grid(row=1, column=2, padx=5, pady=5)
        self.handwrite_btn = customtkinter.CTkButton(self.main_frame, text='handwrite')
        self.handwrite_btn.grid(row=1, column=3, padx=5, pady=5)
        # view 1 frame in main frame
        self.view1_frame = customtkinter.CTkFrame(self.main_frame)
        # view 2 frame in main frame
        
        

        # sub frame , output log , Quit btn, setting slider *2 

        self.log_tb = customtkinter.CTkTextbox(self.sub_frame, width=500, height=80)
        self.log_tb.grid(row=0, column=0, rowspan=2, padx=5, pady=5, sticky='ew')
        self.slider_threshold_1 = customtkinter.CTkSlider(self.sub_frame, from_=0, to=600, number_of_steps=600)
        self.slider_threshold_1.grid(row=0, column=1, padx=5, pady=5)
        self.slider_threshold_2 = customtkinter.CTkSlider(self.sub_frame, from_=0, to=600, number_of_steps=600)
        self.slider_threshold_2.grid(row=1, column=1, padx=5, pady=5)
        self.quit_btn = customtkinter.CTkButton(self.sub_frame, text='Quit')
        self.quit_btn.grid(row=0, column=2, rowspan=2)


        # initial set


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
