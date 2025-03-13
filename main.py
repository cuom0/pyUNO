import customtkinter as ctk
from PIL import Image
import webbrowser  
import game 


homescreen = ctk.CTk()
homescreen.geometry("1000x600")
ctk.set_default_color_theme("dark-blue")
homescreen.configure(fg_color="#094c7d")
homescreen.title("pyUNO")
homescreen.resizable(0, 0)


for i in range(4): # Configuring the grid layout
    homescreen.grid_columnconfigure(i, weight=1)

def show_frame(frame): # A function to show a frame and hide the others
    frame.tkraise()  
    
def close_program():
    homescreen.destroy()
    
def start_game():
    homescreen.destroy()
    game.start_game()

def open_github():
    webbrowser.open("https://github.com/cuom0")

# Home Frame
home_frame = ctk.CTkFrame(homescreen, fg_color="transparent", width=1000, height=600)
home_frame.grid(row=0, column=0, sticky="nsew")

title = ctk.CTkLabel(home_frame, text="pyUNO", fg_color="transparent", font=("Impact", 40), text_color="white")
title.grid(row=0, column=0, columnspan=3, padx=30, pady=15, sticky="n")

play = ctk.CTkButton(home_frame, text="Play!", font=("Arial", 45), width=400, height=90, corner_radius=20, command=start_game)
play.grid(row=1, column=0, columnspan=3, padx=30, pady=5, sticky="n")

credits = ctk.CTkButton(home_frame, text="Credits", font=("Arial", 25), width=300, height=70, corner_radius=15,
                         command=lambda: show_frame(credit_frame))
credits.grid(row=2, column=0, columnspan=3, pady=5, sticky="n")

exit_btn = ctk.CTkButton(home_frame, text="Exit", font=("Arial", 25), width=300, height=70, corner_radius=15,
                         command=close_program)
exit_btn.grid(row=3, column=0, columnspan=3, pady=5, sticky="n")

bgcards = ctk.CTkImage(light_image=Image.open("./media/home/background.png"),
                        dark_image=Image.open("./media/home/background.png"),
                        size=(500, 400))
bgcardslabel = ctk.CTkLabel(home_frame, image=bgcards, text="")
bgcardslabel.grid(row=0, column=3, rowspan=4, padx=(20, 50), pady=50, sticky="e")

# Frame Credits
credit_frame = ctk.CTkFrame(homescreen, fg_color="transparent", width=1000, height=600)
credit_frame.grid(row=0, column=0, sticky="nsew")

ctk.CTkLabel(credit_frame, text="Credits", font=("Impact", 40), text_color="white").pack(pady=20)


ctk.CTkLabel(credit_frame, text="Salvatore Cuomo\n(Lead Developer, Game Designer)", font=("Arial", 30), text_color="white").pack(pady=5)

github_profile_image = ctk.CTkImage(light_image=Image.open("./media/home/githubpfp.jpg"), 
                                    dark_image=Image.open("./media/home/githubpfp.jpg"),
                                    size=(50, 50))
github_button = ctk.CTkButton(credit_frame, text="GitHub", font=("Arial", 20), image=github_profile_image, compound="left", command=open_github)
github_button.pack(pady=5)

ctk.CTkLabel(credit_frame, text="Francesco Ciampa\n(Card Design, PowerPoint)", font=("Arial", 20), text_color="white").pack(pady=10)
ctk.CTkLabel(credit_frame, text="Antonio De Cicco\n(Ideas, PowerPoint)", font=("Arial", 20), text_color="white").pack(pady=10)


back_button = ctk.CTkButton(credit_frame, text="Back", font=("Arial", 25), width=200, height=50, corner_radius=15,
                            command=lambda: show_frame(home_frame))
back_button.pack(pady=20)


home_frame.tkraise() # Makes the home frame visible by default

homescreen.mainloop()
