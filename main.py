import customtkinter
from PIL import Image

homescreen = customtkinter.CTk()
homescreen.geometry("1000x600")

homescreen.configure(fg_color="#094c7d")
homescreen.title("pyUNO: Home Screen")

homescreen.resizable(0, 0)

homescreen.grid_columnconfigure(0, weight=1)
homescreen.grid_columnconfigure(1, weight=1)
homescreen.grid_columnconfigure(2, weight=1)
homescreen.grid_columnconfigure(3, weight=1)

def closeprogram():
    homescreen.destroy()

title = customtkinter.CTkLabel(homescreen, text="pyUNO", fg_color="transparent", font=("Impact", 40), text_color="white")
title.grid(row=0, column=0, columnspan=3, padx=30, pady=15, sticky="n")

play = customtkinter.CTkButton(homescreen, text="Play!")
play.grid(row=1, column=0, columnspan=3, padx=30, pady=5, sticky="n")

credits = customtkinter.CTkButton(homescreen, text="Credits")
credits.grid(row=2, column=0, columnspan=3, pady=5, sticky="n")

exit = customtkinter.CTkButton(homescreen, text="Exit", command=closeprogram)
exit.grid(row=3, column=0, columnspan=3, pady=5, sticky="n")


bgcards = customtkinter.CTkImage(light_image=Image.open("./media/home/background.png"),
                                  dark_image=Image.open("./media/home/background.png"),
                                  size=(500, 400))
bgcardslabel = customtkinter.CTkLabel(homescreen, image=bgcards, text="")
bgcardslabel.grid(row=0, column=3, rowspan=4, padx=(20, 50), pady=50, sticky="e") 

homescreen.mainloop()