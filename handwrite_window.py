#!/usr/bin/env python3
# -*- coding:utf-8 -*-
""" handwrite

    handwrite

"""

import os, sys, glob, datetime
import customtkinter

from logging import INFO, basicConfig, getLogger

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
logger = getLogger(__name__)


class HandWriteWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # init datas
        self.line_datas = []
        self.line_data = []

        # configure window
        self.title("CustomTkinter window")
        self.geometry(f"{1200}x{720}")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure([0, 1, 2], weight=1)
        self.header_frame = customtkinter.CTkFrame(master=self, width=1200, height=110, corner_radius=0,fg_color='red')
        #self.main_frame = customtkinter.CTkFrame(master=self, width=1200, height=500, corner_radius=0)
        self.sub_frame = customtkinter.CTkFrame(master=self, width=1200, height=110, corner_radius=0,fg_color='green')
        self.header_frame.grid(row=0, column=0, sticky="nsew")
        #self.main_frame.grid(row=1, column=0, sticky="nsew")
        self.sub_frame.grid(row=2, column=0, sticky="nsew")

        
        self.header_label = customtkinter.CTkLabel(self.header_frame, text='Test Drawing canvas')
        self.header_label.grid(row=0, column=0, sticky="nsew")
        #self.main_frame.grid_columnconfigure(0, weight=1)
        #self.main_frame.grid_rowconfigure(0, weight=1)
        self.canvas = customtkinter.CTkCanvas(self, highlightthickness=0, width=1200, height=500)
        self.canvas.grid(row=1, column=0, sticky="nsew")

        self.sub_frame.grid_columnconfigure([0, 1, 2], weight=1)
        self.sub_frame.grid_rowconfigure(0, weight=1)
        self.undo_btn = customtkinter.CTkButton(self.sub_frame, text='Undo', command=self.undo_func)
        self.clear_btn = customtkinter.CTkButton(self.sub_frame, text='clear', command=self.clear_func)
        self.start_btn = customtkinter.CTkButton(self.sub_frame, text='start', command=self.start_func)
        self.undo_btn.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.clear_btn.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.start_btn.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        self.canvas.bind('<ButtonPress-1>', self.event_click)
        self.canvas.bind('<ButtonRelease-1>', self.event_release)
        self.canvas.bind('<B1-Motion>', self.event_motion)
        self.canvas.bind('<Leave>', self.event_leave)

    def start_func(self):
        pass
    # End def
    def undo_func(self):
        self.canvas.delete('all')
        if len(self.line_datas) > 0:
            self.line_datas.pop(-1)
            for data in self.line_datas:
                self.canvas.create_line(data, fill='black', width=1)
            # End for
        # End if
    # End def
    def clear_func(self):
        self.canvas.delete('all')
        self.line_datas.clear()
    # End func

    def event_click(self, event):
        print(f'Click , x={event.x}, y={event.y}')
        self.line_data.append([event.x, event.y])
    def event_release(self, event):
        if len(self.line_data) > 0:
            print(f'Release , x={event.x}, y={event.y}')
            last_point = self.line_data[-1]
            cur_point = [event.x, event.y]
            self.canvas.create_line(last_point[0], last_point[1], cur_point[0], cur_point[1], fill='black', width=1)
            self.line_data.append(cur_point)
            self.line_datas.append(self.line_data)
            self.line_data = []
        # End if
    def event_leave(self, event):
        print(f'Leave , x={event.x}, y={event.y}')
        if len(self.line_data) > 0:
            self.line_datas.append(self.line_data)
            self.line_data = []
        # End if
    def event_motion(self, event):
        cur_point = [event.x, event.y]
        if len(self.line_data) > 0:
            last_point = self.line_data[-1]
            self.canvas.create_line(last_point[0], last_point[1], cur_point[0], cur_point[1], fill='black', width=1)
            self.line_data.append(cur_point)
        # End if
        print(f'motion [x,y] = {cur_point}')

def main():
    os.makedirs(os.path.join(os.path.dirname(sys.argv[0]), "log"), exist_ok=True)
    basicConfig(level=INFO, filename=os.path.join(os.path.dirname(sys.argv[0]), "log", "handwrite.log"), format="%(asctime)s:%(levelname)s:%(message)s ")
    logger.info('handwritewin rogs')
    app = HandWriteWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
