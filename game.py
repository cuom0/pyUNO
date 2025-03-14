import customtkinter
from PIL import Image
import customtkinter as ctk



game_window = customtkinter.CTk()
game_window.geometry("1200x800")
game_window.title("pyUNO")
    
classic_image = ctk.CTkImage(light_image=Image.open("./media/home/classic.png"), 
                                 dark_image=Image.open("./media/home/classic.png"),
                                 size=(100, 100))
hard_image = ctk.CTkImage(light_image=Image.open("./media/home/hardmode.png"), 
                              dark_image=Image.open("./media/home/hardmode.png"),
                              size=(100, 100))

    
game_window.grid_rowconfigure(0, weight=1)
game_window.grid_rowconfigure(1, weight=1)
game_window.grid_columnconfigure(0, weight=1)
game_window.grid_columnconfigure(1, weight=1)
game_window.grid_columnconfigure(2, weight=1)
    
gamemode_label = ctk.CTkLabel(game_window, text="Game Mode", font=("Impact", 40), text_color="white")
gamemode_label.grid(row=0, column=1, pady=10, sticky="n")  # Adjusted pady


classic_button = ctk.CTkButton(game_window, text="Classic Mode", font=("Arial", 25), image=classic_image, compound="top", width=400, height=300, corner_radius=20)
classic_button.grid(row=1, column=0, padx=50, pady=10, sticky="e")

hard_button = ctk.CTkButton(game_window, text="HARD MODE", font=("Arial", 25), text_color="red", image=hard_image, compound="top", width=400, height=300, corner_radius=20)
hard_button.grid(row=1, column=2, padx=50, pady=0, sticky="w")
    
game_window.mainloop()