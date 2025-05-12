import customtkinter as ctk
from PIL import Image
from card import Card
import random

class Game:
    def __init__(self):
        self.deck = self._create_deck()
        self.discard_pile = []
        self.current_player = 0
        self.players = [[], [], []]  # player, AI1, AI2 hands
        self.direction = 1  # 1 for clockwise, -1 for counter-clockwise

    def _create_deck(self):
        deck = []
        colors = ["Red", "Blue", "Green", "Yellow"]
        numbers = list(range(0, 10)) + list(range(1, 10))  # 0-9 once, 1-9 twice
        
        # Add number cards
        for color in colors:
            for number in numbers:
                deck.append(Card(color, str(number)))
        
        # Add special cards (Skip, Reverse, +2)
        special_cards = ["Skip", "Reverse", "+2"]
        for color in colors:
            for _ in range(2):  # Two of each special card per color
                for special in special_cards:
                    deck.append(Card(color, special))
        
        # Add wild cards
        for _ in range(4):  # Four of each wild card
            deck.append(Card("Black", "Wild"))
            deck.append(Card("Black", "+4"))
        
        random.shuffle(deck)
        return deck

    def draw_card(self):
        """Draw a card from the deck"""
        if not self.deck:
            if self.discard_pile:
                last_card = self.discard_pile.pop()
                self.deck = self.discard_pile
                self.discard_pile = [last_card]
                random.shuffle(self.deck)
            else:
                return None
        return self.deck.pop()

    def play_card(self, card):
        """Play a card to the discard pile"""
        self.discard_pile.append(card)

    def is_valid_play(self, card):
        """Check if a card can be played"""
        if not self.discard_pile:
            return True
        
        top_card = self.discard_pile[-1]
        
        if card.color == "Black":
            return True
            
        return (card.color == top_card.color or 
                card.value == top_card.value)

    def next_turn(self):
        """Move to the next player's turn"""
        self.current_player = (self.current_player + self.direction) % 3
        return self.current_player

class GameManager:
    def __init__(self, game_frame, ui_elements):
        self.game_frame = game_frame
        self.ui_elements = ui_elements
        self.game = Game()
        self.player_hand = []
        self.uno_called = False
        self.ai_thinking = False
        # Add after delay between AI moves (in milliseconds)
        self.ai_delay = 1000
        self.waiting_for_color = False
        self.temp_wild_card = None

    def initialize_game(self):
        """Initialize the game state and deal initial cards"""
        # Deal initial cards
        for _ in range(7):
            self.player_hand.append(self.game.draw_card())
            self.game.players[1].append(self.game.draw_card())  # AI 1
            self.game.players[2].append(self.game.draw_card())  # AI 2
        
        # Update the display
        self.update_game_state()
        self.update_ai_labels()

    def update_game_state(self):
        """Update the game state display"""
        try:
            self.update_player_hand()
            self.update_ai_labels()
            
            # Update last played card if exists
            if self.game.discard_pile:
                last_card = self.game.discard_pile[-1]
                self.ui_elements['last_card'].configure(
                    image=last_card.get_image((150, 225))
                )
            
            # Update turn indicator
            turn_text = "Your Turn" if self.game.current_player == 0 else f"AI {self.game.current_player}'s Turn"
            self.ui_elements['turn_label'].configure(text=turn_text)
            
            # Update UNO button state
            self.ui_elements['uno_button'].configure(
                state="normal" if len(self.player_hand) == 2 else "disabled"
            )
            
            # Force update
            self.game_frame.update()
        except Exception as e:
            print(f"Error updating game state: {str(e)}")

    def update_player_hand(self):
        """Update the display of player's hand"""
        card_holder = self.ui_elements['card_holder']
        
        # Clear existing cards
        for widget in card_holder.winfo_children():
            widget.destroy()
            
        # Add current cards
        for card in self.player_hand:
            card_btn = ctk.CTkButton(
                card_holder,
                image=card.get_image((100, 150)),
                text="",
                width=100,
                command=lambda c=card: self.play_card(c)
            )
            card_btn.pack(side="left", padx=5)

    def update_ai_labels(self):
        """Update AI card count labels"""
        self.ui_elements['ai1_label'].configure(
            text=f"AI 1\n{len(self.game.players[1])} Cards"
        )
        self.ui_elements['ai2_label'].configure(
            text=f"AI 2\n{len(self.game.players[2])} Cards"
        )

    def draw_card(self):
        """Handle drawing a card"""
        if self.game.current_player == 0:  # Only allow drawing on player's turn
            new_card = self.game.draw_card()
            if new_card:
                self.player_hand.append(new_card)
                self.update_game_state()
                self.game.next_turn()
                self.update_game_state()

    def handle_wild_card(self, card):
        """Handle wild card color selection for player"""
        self.waiting_for_color = True
        self.temp_wild_card = card
        
        # Create color selection popup
        color_popup = ctk.CTkFrame(self.game_frame, fg_color="#553D24")
        color_popup.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(
            color_popup, 
            text="Choose a color:", 
            font=("Arial", 20)
        ).pack(pady=10)
        
        colors = ["Red", "Blue", "Green", "Yellow"]
        color_hex = {"Red": "#FF0000", "Blue": "#0000FF", 
                    "Green": "#00FF00", "Yellow": "#FFFF00"}
        
        for color in colors:
            ctk.CTkButton(
                color_popup,
                text=color,
                fg_color=color_hex[color],
                text_color="black",
                command=lambda c=color: self.complete_wild_card_play(c, color_popup)
            ).pack(pady=5, padx=20)

    def complete_wild_card_play(self, chosen_color, popup):
        """Complete wild card play after color selection"""
        popup.destroy()
        self.waiting_for_color = False
        self.temp_wild_card.color = chosen_color
        self.player_hand.remove(self.temp_wild_card)
        self.game.play_card(self.temp_wild_card)
        self.update_game_state()
        self.game.next_turn()
        self.game_frame.after(500, self.handle_ai_turn)

    def ai_choose_wild_color(self, ai_number):
        """AI chooses color based on its hand"""
        ai_hand = self.game.players[ai_number]
        color_counts = {"Red": 0, "Blue": 0, "Green": 0, "Yellow": 0}
        
        # Count colors in AI's hand
        for card in ai_hand:
            if card.color in color_counts:
                color_counts[card.color] += 1
        
        # Choose most frequent color
        chosen_color = max(color_counts.items(), key=lambda x: x[1])[0]
        
        # Show popup with AI's choice
        color_popup = ctk.CTkFrame(self.game_frame, fg_color="#553D24")
        color_popup.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(
            color_popup,
            text=f"AI {ai_number} chose {chosen_color}",
            font=("Arial", 20)
        ).pack(pady=20, padx=40)
        
        # Auto-close popup after 1.5 seconds
        self.game_frame.after(1500, color_popup.destroy)
        
        return chosen_color

    def play_card(self, card):
        """Handle playing a card"""
        if self.game.current_player == 0 and not self.waiting_for_color:  # Player's turn
            if self.game.is_valid_play(card):
                if len(self.player_hand) == 2 and not self.uno_called:
                    return
                
                if card.value in ["Wild", "+4"]:
                    self.handle_wild_card(card)
                    return
                
                self.player_hand.remove(card)
                self.game.play_card(card)
                self.update_game_state()
                
                self.uno_called = False
                
                if len(self.player_hand) == 0:
                    self.game_won()
                    return
                
                self.game.next_turn()
                self.update_game_state()
                self.game_frame.after(500, self.handle_ai_turn)

    def handle_ai_turn(self):
        """Handle AI turns"""
        while self.game.current_player != 0:
            current_ai = self.game.current_player
            ai_hand = self.game.players[current_ai]
            
            # Find valid card to play
            valid_card = None
            for card in ai_hand:
                if self.game.is_valid_play(card):
                    valid_card = card
                    break
            
            if valid_card:
                ai_hand.remove(valid_card)
                
                # Handle wild card played by AI
                if valid_card.value in ["Wild", "+4"]:
                    chosen_color = self.ai_choose_wild_color(current_ai)
                    valid_card.color = chosen_color
                
                self.game.play_card(valid_card)
                self.update_ai_labels()
                
                if len(ai_hand) == 0:
                    self.ai_won(current_ai)
                    return
            else:
                new_card = self.game.draw_card()
                if new_card:
                    ai_hand.append(new_card)
            
            self.update_game_state()
            self.game.next_turn()
            
            if self.game.current_player != 0:
                self.game_frame.after(self.ai_delay, self.handle_ai_turn)
                return

    def ai_won(self, ai_number):
        """Handle AI win condition"""
        win_frame = ctk.CTkFrame(self.game_frame)
        win_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        win_label = ctk.CTkLabel(
            win_frame, 
            text=f"AI {ai_number} Won!", 
            font=("Impact", 40)
        )
        win_label.pack(pady=20, padx=40)

    def call_uno(self):
        """Handle UNO button press"""
        if len(self.player_hand) == 2:
            self.uno_called = True
            self.ui_elements['uno_button'].configure(state="disabled")

    def game_won(self):
        """Handle game win condition"""
        win_frame = ctk.CTkFrame(self.game_frame)
        win_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        win_label = ctk.CTkLabel(
            win_frame, 
            text="You Won!", 
            font=("Impact", 40)
        )
        win_label.pack(pady=20, padx=40)