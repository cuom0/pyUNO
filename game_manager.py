import customtkinter as ctk
from card import Game, Card
import random

class GameManager:
    def __init__(self, game_frame):
        self.game_frame = game_frame
        self.game = Game(4)  # 1 player + 3 AI
        self.card_buttons = []
        
        # Initialize UI element references
        self.card_holder = None
        self.deck_label = None
        self.last_card_label = None
        self.turn_label = None
        self.ai1_frame = None
        self.ai2_frame = None
        self.uno_button = None
        
        self.setup_game_ui()
        self.setup_color_selector()
        self.update_game_state()
        
    def setup_game_ui(self):
        # Find all UI elements by searching through children
        for child in self.game_frame.winfo_children():
            if isinstance(child, ctk.CTkScrollableFrame):
                self.card_holder = child
                continue
                
            if isinstance(child, ctk.CTkButton) and child._text == "UNO!":
                self.uno_button = child
                continue
                
            if isinstance(child, ctk.CTkLabel):
                if child._text == "Your Turn":
                    self.turn_label = child
                elif child._text == "":  # Image labels have empty text
                    if not self.deck_label:
                        self.deck_label = child
                    else:
                        self.last_card_label = child
                continue
                
            if isinstance(child, ctk.CTkFrame):
                for subchild in child.winfo_children():
                    if isinstance(subchild, ctk.CTkLabel):
                        if "AI 1" in subchild._text:
                            self.ai1_frame = subchild
                        elif "AI 2" in subchild._text:
                            self.ai2_frame = subchild
        
        # Make deck clickable
        if self.deck_label:
            self.deck_label.configure(cursor="hand2")
            self.deck_label.bind("<Button-1>", lambda e: self.draw_card())

    def setup_color_selector(self):
        self.color_frame = ctk.CTkFrame(self.game_frame, fg_color="#333333")
        ctk.CTkLabel(self.color_frame, text="Choose a color:", 
                     font=("Arial", 24), text_color="white").pack(pady=10)
        
        colors = [
            ("Red", "#FF0000"), 
            ("Blue", "#0000FF"),
            ("Green", "#00FF00"), 
            ("Yellow", "#FFD700")
        ]
        
        for color_name, color_code in colors:
            btn = ctk.CTkButton(
                self.color_frame,
                text=color_name,
                font=("Arial", 20),
                fg_color=color_code,
                hover_color=color_code,
                command=lambda c=color_name.lower(): self.handle_color_selection(c)
            )
            btn.pack(pady=5, padx=20)

    def update_game_state(self):
        if self.game.discard_pile:
            top_card = self.game.discard_pile[-1]
            if self.last_card_label:
                self.last_card_label.configure(image=top_card.get_image())
        
        self.update_player_hand()
        self.update_ai_info()
        
    def update_player_hand(self):
        if not self.card_holder:
            return
            
        for widget in self.card_holder.winfo_children():
            widget.destroy()
            
        for card in self.game.players[0]:
            card_btn = ctk.CTkButton(
                self.card_holder,
                image=card.get_image((100, 150)),
                text="",
                width=100,
                command=lambda c=card: self.play_card(c)
            )
            card_btn.pack(side="left", padx=5)
            
    def update_ai_info(self):
        if self.ai1_frame:
            self.ai1_frame.configure(text=f"AI 1\n{len(self.game.players[1])} Cards")
        if self.ai2_frame:
            self.ai2_frame.configure(text=f"AI 2\n{len(self.game.players[2])} Cards")
            
    def handle_color_selection(self, color):
        self.color_frame.place_forget()
        self.game.discard_pile[-1].color = color
        self.game.next_turn()
        self.ai_turns()

    def draw_card(self):
        if self.game.current_player == 0:  # Only allow drawing on player's turn
            drawn_card = self.game.deck.draw()
            if drawn_card:
                # Add card to player's hand regardless of playability
                self.game.players[0].append(drawn_card)
                self.update_player_hand()
                
                # Check if drawn card is playable
                top_card = self.game.discard_pile[-1]
                if not (drawn_card.color == top_card.color or 
                       drawn_card.value == top_card.value or 
                       drawn_card.color == 'black'):
                    # Card not playable, keep it and end turn
                    self.game.next_turn()
                    self.ai_turns()
            # If card is playable, player can choose to play it
    
    def play_card(self, card):
        if self.game.current_player == 0:
            player_hand = self.game.players[0]
            card_idx = player_hand.index(card)
            
            if self.game.play_card(0, card_idx):
                self.update_game_state()
                
                # Check for wild cards
                if card.color == 'black':
                    self.show_color_selector()
                    return  # Wait for color selection
                    
                self.check_win()
                self.ai_turns()
                
    def ai_turns(self):
        self.turn_label.configure(text="AI's Turn")
        self.game_frame.after(1000)  # Add 1 second delay
        
        while self.game.current_player != 0 and not self.check_win():
            ai_idx = self.game.current_player
            ai_hand = self.game.players[ai_idx]
            
            # Simple AI: play first valid card
            played = False
            for card_idx, card in enumerate(ai_hand):
                if self.game.is_valid_play(card):
                    self.game.play_card(ai_idx, card_idx)
                    played = True
                    
                    # Handle AI wild card
                    if card.color == 'black':
                        colors = ["red", "blue", "green", "yellow"]
                        chosen_color = random.choice(colors)
                        self.game.discard_pile[-1].color = chosen_color
                        
                        # Show temporary color notification
                        notification = ctk.CTkLabel(
                            self.game_frame,
                            text=f"AI chose {chosen_color}!",
                            font=("Arial", 24),
                            fg_color="black"
                        )
                        notification.place(relx=0.5, rely=0.3, anchor="center")
                        self.game_frame.after(2000, notification.destroy)  # Remove after 2 seconds
                    
                    break
            
            if not played:
                drawn_card = self.game.deck.draw()
                if drawn_card:
                    ai_hand.append(drawn_card)
                self.game.next_turn()
            
            self.update_game_state()
            self.game_frame.update()
            self.game_frame.after(1000)  # Add 1 second delay between AI moves
        
        self.turn_label.configure(text="Your Turn")
        
    def check_win(self):
        for i, hand in enumerate(self.game.players):
            if len(hand) == 0:
                winner = "You" if i == 0 else f"AI {i}"
                self.show_game_over(winner)
                return True
        return False
    
    def show_game_over(self, winner):
        game_over = ctk.CTkFrame(self.game_frame, fg_color="black")
        game_over.place(relx=0.5, rely=0.5, anchor="center")
        
        message = ctk.CTkLabel(
            game_over, 
            text=f"{winner} won the game!", 
            font=("Impact", 40),
            text_color="white"
        )
        message.pack(pady=20, padx=40)
    
    def show_color_selector(self):
        self.color_frame.place(relx=0.5, rely=0.5, anchor="center")