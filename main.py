import customtkinter as ctk
from PIL import Image
import webbrowser  
from game_manager import GameManager

homescreen = ctk.CTk()
homescreen.geometry("1000x600")
ctk.set_default_color_theme("dark-blue")
homescreen.resizable(False, False)
homescreen.configure(fg_color="#094c7d")
homescreen.title("pyUNO")

def show_frame(frame): 
    frame.tkraise()
    frame.update()  # Force update to show frame immediately

for i in range(4): 
    homescreen.grid_columnconfigure(i, weight=1)

def close_program():
    homescreen.destroy()
    
def start_game(): #Da fixare le tre CPU nell'UI
    game_frame = ctk.CTkFrame(homescreen, fg_color="#92663E")
    game_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    # Create dictionary to store UI elements
    ui_elements = {}
    
    # Create all UI elements first
    ui_elements['card_holder'] = ctk.CTkScrollableFrame(
        game_frame, width=700, height=120, 
        orientation="horizontal", fg_color="#6B4B2D"
    )
    ui_elements['card_holder'].place(relx=0.5, rely=0.85, anchor="center")

    # UNO button
    ui_elements['uno_button'] = ctk.CTkButton(
        game_frame, height=100, width=150, font=("Impact", 65), text="UNO!", 
        fg_color="#CC2E2E", hover_color="#ff0000", state="disabled",
        command=lambda: game_manager.call_uno()  # Add this line
    )
    ui_elements['uno_button'].place(relx=0.9, rely=0.85, anchor="center")

    # Deck and last card
    deck_img = ctk.CTkImage(light_image=Image.open("./media/cards/pyUNO Retro.png"),
                           dark_image=Image.open("./media/cards/pyUNO Retro.png"),
                           size=(150, 225))

    ui_elements['deck_label'] = ctk.CTkLabel(game_frame, image=deck_img, text="")
    ui_elements['deck_label'].place(relx=0.4, rely=0.4, anchor="center")
    
    ui_elements['last_card'] = ctk.CTkLabel(game_frame, image=deck_img, text="")
    ui_elements['last_card'].place(relx=0.6, rely=0.4, anchor="center")

    # Turn indicator
    ui_elements['turn_label'] = ctk.CTkLabel(
        game_frame, text="Your Turn", font=("Impact", 30), text_color="white"
    )
    ui_elements['turn_label'].place(relx=0.5, rely=0.15, anchor="center")

    # AI info
    ai1_frame = ctk.CTkFrame(game_frame, fg_color="#553D24")
    ai1_frame.place(relx=0.1, rely=0.4, anchor="center")
    ui_elements['ai1_label'] = ctk.CTkLabel(
        ai1_frame, text="AI 1\n7 Cards", font=("Arial", 24), text_color="white"
    )
    ui_elements['ai1_label'].pack(pady=10, padx=20)

    ai2_frame = ctk.CTkFrame(game_frame, fg_color="#553D24")
    ai2_frame.place(relx=0.9, rely=0.4, anchor="center")
    ui_elements['ai2_label'] = ctk.CTkLabel(
        ai2_frame, text="AI 2\n7 Cards", font=("Arial", 24), text_color="white"
    )
    ui_elements['ai2_label'].pack(pady=10, padx=20)

    # Initialize game manager with UI elements dictionary
    game_manager = GameManager(game_frame, ui_elements)
    
    # Configure deck label to draw cards
    ui_elements['deck_label'].bind('<Button-1>', lambda e: game_manager.draw_card())
    
    # Initialize the game state
    game_manager.initialize_game()
    
    return game_frame

def open_github():
    webbrowser.open("https://github.com/cuom0")

# Home Frame
home_frame = ctk.CTkFrame(homescreen, fg_color="transparent", width=1000, height=600)
home_frame.grid(row=0, column=0, sticky="nsew") # The frame is placed in the grid layout and set to fill the window

title = ctk.CTkLabel(home_frame, text="pyUNO", fg_color="transparent", font=("Impact", 40), text_color="white")
title.grid(row=0, column=0, columnspan=3, padx=30, pady=15, sticky="n")

play = ctk.CTkButton(home_frame, text="Play!", font=("Arial", 45), width=400, height=90, corner_radius=20, command=lambda: show_frame(mode_selector))
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

# Mode Selector Frame
mode_selector = ctk.CTkFrame(homescreen, fg_color="transparent", width=1000, height=800)
mode_selector.grid(row=0, column=0, sticky="nsew")

classic_image = ctk.CTkImage(light_image=Image.open("./media/home/classic.png"), 
                             dark_image=Image.open("./media/home/classic.png"),
                             size=(100, 100))
hard_image = ctk.CTkImage(light_image=Image.open("./media/home/hardmode.png"), 
                          dark_image=Image.open("./media/home/hardmode.png"),
                          size=(100, 100))

mode_selector.grid_rowconfigure(0, weight=1)
mode_selector.grid_rowconfigure(1, weight=1)
mode_selector.grid_columnconfigure(0, weight=1)
mode_selector.grid_columnconfigure(1, weight=1)
mode_selector.grid_columnconfigure(2, weight=1)
        
gamemode_label = ctk.CTkLabel(mode_selector, text="Game Mode", font=("Impact", 40), text_color="white")
gamemode_label.grid(row=0, column=1, pady=10, sticky="n")
goback = ctk.CTkButton(mode_selector, text="Back", font=("Arial", 25), width=200, height=50, corner_radius=15,
                       command=lambda: show_frame(home_frame))
goback.grid(row=0, column=2, padx=2.5, pady=10, sticky="en")


def start_classic_game():
    game_frame = start_game()
    show_frame(game_frame)
    homescreen.update()

classic_button = ctk.CTkButton(mode_selector, text="Classic Mode", font=("Arial", 25), 
                              image=classic_image, compound="top", width=400, height=300, 
                              corner_radius=20, command=start_classic_game)
classic_button.grid(row=1, column=0, padx=2.5, pady=0, sticky="e")  # Add this line

def show_coming_soon():
    coming_soon_label = ctk.CTkLabel(mode_selector, text="Coming soon!", font=("Arial", 20), text_color="white")
    coming_soon_label.grid(row=2, column=2, pady=10, sticky="n")

hard_button = ctk.CTkButton(mode_selector, text="HARD MODE", font=("Arial", 25), text_color="red", image=hard_image, compound="top", width=400, height=300, corner_radius=20, command=show_coming_soon)
hard_button.grid(row=1, column=2, padx=2.5, pady=0, sticky="w")

home_frame.tkraise() # Makes the home frame visible by default

homescreen.mainloop()
