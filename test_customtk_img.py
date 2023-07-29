import customtkinter
import os
from PIL import Image

app = customtkinter.CTk()
app.geometry("400x200+50+50")
app.title("Image")

dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
logo_image = customtkinter.CTkImage(Image.open(os.path.join(dir_path,"testimg.jpg")),size=(64, 64))
label = customtkinter.CTkLabel(app, text="　Custom Tkinter",image=logo_image, compound="left", font=customtkinter.CTkFont(size=20, weight="bold"))
label.pack()

app.mainloop()