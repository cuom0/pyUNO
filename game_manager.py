import customtkinter as ctk
from PIL import Image
import random
from card import Card

class GameManager:
    def __init__(self, game_frame, ui_elements):
        self.player_hand = []
        self.ai_hands = [[], []]  # AI1 and AI2 hands
        self.deck = self._create_deck()
        self.discard_pile = []
        self.current_player = 0
        self.direction = 1
        self.uno_called = False
        self.waiting_for_color = False
        self.ai_delay = 2000  # Increased to 2 seconds for better visibility
        self.game_frame = game_frame
        self.ui_elements = ui_elements

    def _create_deck(self):
        deck = []
        colors = ["Red", "Blue", "Green", "Yellow"]
        numbers = [str(n) for n in list(range(10)) + list(range(1, 10))]
        specials = ["Skip", "Reverse", "+2"]
        
        for color in colors:
            for num in numbers:
                deck.append(Card(color, num))
            
            for _ in range(2):  # Two of each special card
                for special in specials:
                    deck.append(Card(color, special))
        
        for _ in range(4):  # Four of each wild card
            deck.append(Card("Black", "Wild"))
            deck.append(Card("Black", "+4"))
        
        random.shuffle(deck)
        return deck

    def initialize_game(self):
        # Deal initial cards
        for _ in range(7):
            self.player_hand.append(self.deck.pop())
            self.ai_hands[0].append(self.deck.pop())
            self.ai_hands[1].append(self.deck.pop())
        
        # Initial card (not wild)
        while True:
            card = self.deck.pop()
            if card.color != "Black":
                self.discard_pile.append(card)
                break
            self.deck.append(card)
            random.shuffle(self.deck)
        
        self.update_game_state()

    def handle_wild_card(self, card):
        """Handle wild card color selection"""
        self.waiting_for_color = True
        
        popup = ctk.CTkFrame(self.game_frame, fg_color="#553D24")
        popup.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(popup, text="Choose a color:", 
                    font=("Arial", 20)).pack(pady=10)
        
        colors = {
            "Red": "#FF0000",
            "Blue": "#0000FF",
            "Green": "#00FF00",
            "Yellow": "#FFFF00"
        }
        
        for color, hex_color in colors.items():
            btn = ctk.CTkButton(
                popup,
                text=color,
                fg_color=hex_color,
                text_color="black",
                command=lambda c=color: self.complete_wild_card_play(card, c, popup)
            )
            btn.pack(pady=5, padx=20)

    def complete_wild_card_play(self, card, chosen_color, popup, win_pending=False):
        """Complete playing a wild card after color is chosen"""
        card.color = chosen_color
        self.discard_pile.append(card)
        popup.destroy()
        self.waiting_for_color = False
        
        if win_pending:
            self.game_won()
            return
            
        if card.value == "+4":
            self.handle_special_card(card)
        else:
            self.current_player = (self.current_player + self.direction) % 3
        
        self.game_frame.after(500, self.handle_ai_turn)
        self.update_game_state()

    def is_valid_play(self, card):
        """Check if a card can be played"""
        if not self.discard_pile:
            return True
            
        top_card = self.discard_pile[-1]
        
        # Wild cards can always be played
        if card.color == "Black":
            return True
            
        # If top card is wild, match its chosen color
        if top_card.color != "Black":
            return card.color == top_card.color or card.value == top_card.value
            
        return False  # Shouldn't reach here

    def update_game_state(self):
        """Update all UI elements"""
        try:
            # Update player's hand
            self.update_player_hand()
            
            # Update discard pile top card
            if self.discard_pile:
                top_card = self.discard_pile[-1]
                self.ui_elements['last_card'].configure(
                    image=top_card.get_image((150, 225))
                )
            
            # Update AI labels
            self.update_ai_labels()
            
            # Update turn indicator
            turn_text = "Your Turn" if self.current_player == 0 else f"AI {self.current_player}'s Turn"
            self.ui_elements['turn_label'].configure(text=turn_text)
            
            # Update UNO button state
            self.ui_elements['uno_button'].configure(
                state="normal" if len(self.player_hand) == 2 else "disabled"
            )
            
            # Force update
            self.game_frame.update()
            
        except Exception as e:
            print(f"Error updating game state: {str(e)}")

    def play_card(self, card):
        """Handle playing a card"""
        if self.current_player == 0 and not self.waiting_for_color:
            if self.is_valid_play(card):
                # Check for UNO button violation
                if len(self.player_hand) == 2 and not self.uno_called:
                    # Player should have called UNO - add 2 cards as penalty
                    for _ in range(2):
                        if self.deck:
                            self.player_hand.append(self.deck.pop())
                    self.update_game_state()
                    return
                
                self.player_hand.remove(card)
                
                # Add card to discard pile before checking win
                if card.color != "Black":
                    self.discard_pile.append(card)
                
                # Check win condition immediately
                if len(self.player_hand) == 0:
                    if card.color == "Black":
                        # For black cards, wait for color selection before winning
                        self.waiting_for_color = True
                        self.show_color_picker(card, win_pending=True)
                    else:
                        self.game_won()
                    return
                
                # Normal card play logic continues...
                if card.color == "Black":
                    self.waiting_for_color = True
                    self.handle_wild_card(card)  # Changed from show_color_picker to handle_wild_card
                else:
                    self.discard_pile.append(card)
                    if card.value in ["Skip", "Reverse", "+2", "+4"]:
                        self.handle_special_card(card)
                    else:
                        self.current_player = (self.current_player + self.direction) % 3
                    self.game_frame.after(500, self.handle_ai_turn)
            
            self.update_game_state()

    def update_player_hand(self):
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
        self.ui_elements['ai1_label'].configure(
            text=f"AI 1\n{len(self.ai_hands[0])} Cards"
        )
        self.ui_elements['ai2_label'].configure(
            text=f"AI 2\n{len(self.ai_hands[1])} Cards"
        )

    def draw_card(self):
        if self.current_player == 0:  # Only allow drawing on player's turn
            if self.deck:
                new_card = self.deck.pop()
                self.player_hand.append(new_card)
                self.update_game_state()
                self.current_player = (self.current_player + self.direction) % 3
                self.game_frame.after(500, self.handle_ai_turn)

    def call_uno(self):
        if len(self.player_hand) == 2:
            self.uno_called = True
            self.ui_elements['uno_button'].configure(state="disabled")
            
    def handle_special_card(self, card):
        """Handle special card effects (+2, Skip, Reverse, +4)"""
        next_player = (self.current_player + self.direction) % 3
        
        if card.value == "Skip":
            self.current_player = (next_player + self.direction) % 3
        elif card.value == "Reverse":
            self.direction *= -1
            self.current_player = (self.current_player + self.direction) % 3
        elif card.value == "+2":
            # Make next player draw 2 cards
            if next_player == 0:
                for _ in range(2):
                    if self.deck:
                        self.player_hand.append(self.deck.pop())
            else:
                for _ in range(2):
                    if self.deck:
                        self.ai_hands[next_player-1].append(self.deck.pop())
            self.current_player = (next_player + self.direction) % 3
        elif card.value == "+4":  # Add this section
            # Make next player draw 4 cards
            if next_player == 0:
                for _ in range(4):
                    if self.deck:
                        self.player_hand.append(self.deck.pop())
            else:
                for _ in range(4):
                    if self.deck:
                        self.ai_hands[next_player-1].append(self.deck.pop())
            self.current_player = (next_player + self.direction) % 3
        else:
            self.current_player = next_player

    def handle_ai_turn(self):
        """Handle AI turns"""
        while self.current_player != 0:
            current_ai = self.current_player - 1  # Convert to 0-based index for ai_hands
            ai_hand = self.ai_hands[current_ai]
            
            # Check for win condition first
            if len(ai_hand) == 0:
                self.ai_won(current_ai + 1)
                return
                
            # Check if deck needs reshuffling
            if not self.deck and self.discard_pile:
                last_card = self.discard_pile.pop()
                self.deck = self.discard_pile[:-1]
                self.discard_pile = [last_card]
                random.shuffle(self.deck)
            
            # Find valid card to play
            valid_card = None
            for card in ai_hand:
                if self.is_valid_play(card):
                    valid_card = card
                    break
            
            if valid_card:
                # AI plays the card
                ai_hand.remove(valid_card)
                
                # Show what card AI played
                play_popup = ctk.CTkFrame(self.game_frame, fg_color="#553D24")
                play_popup.place(relx=0.5, rely=0.5, anchor="center")
                ctk.CTkLabel(
                    play_popup,
                    text=f"AI {current_ai + 1} plays {valid_card.color} {valid_card.value}",
                    font=("Arial", 20)
                ).pack(pady=20, padx=40)
                self.game_frame.after(1500, play_popup.destroy)
                
                # Handle special cards
                if valid_card.color == "Black":
                    colors = {"Red": 0, "Blue": 0, "Green": 0, "Yellow": 0}
                    for card in ai_hand:
                        if card.color in colors:
                            colors[card.color] += 1
                    chosen_color = max(colors.items(), key=lambda x: x[1])[0]
                    
                    # Show color choice
                    popup = ctk.CTkFrame(self.game_frame, fg_color="#553D24")
                    popup.place(relx=0.5, rely=0.5, anchor="center")
                    ctk.CTkLabel(
                        popup,
                        text=f"AI {current_ai + 1} chose {chosen_color}",
                        font=("Arial", 20)
                    ).pack(pady=20, padx=40)
                    self.game_frame.after(1500, popup.destroy)
                    
                    valid_card.color = chosen_color
                
                self.discard_pile.append(valid_card)
                
                # Check win condition after playing card
                if len(ai_hand) == 0:
                    self.ai_won(current_ai + 1)
                    return
                
                # Handle special card effects
                if valid_card.value in ["Skip", "Reverse", "+2", "+4"]:
                    self.handle_special_card(valid_card)
                else:
                    self.current_player = (self.current_player + self.direction) % 3
            else:
                # AI must draw a card
                if self.deck:
                    new_card = self.deck.pop()
                    ai_hand.append(new_card)
                    # Show draw message
                    draw_popup = ctk.CTkFrame(self.game_frame, fg_color="#553D24")
                    draw_popup.place(relx=0.5, rely=0.5, anchor="center")
                    ctk.CTkLabel(
                        draw_popup,
                        text=f"AI {current_ai + 1} draws a card",
                        font=("Arial", 20)
                    ).pack(pady=20, padx=40)
                    self.game_frame.after(1000, draw_popup.destroy)
                else:
                    self.game_draw()
                    return
                self.current_player = (self.current_player + self.direction) % 3
            
            self.update_game_state()
            
            if self.current_player != 0:
                self.game_frame.after(self.ai_delay, self.handle_ai_turn)
                return

    def calculate_score(self, winner):
        """Calculate score based on remaining cards"""
        points = 0
        # Count points from player's hand
        for card in self.player_hand:
            if card.value in ["+4", "Wild"]:
                points += 50
            elif card.value in ["+2", "Skip", "Reverse"]:
                points += 20
            else:
                points += int(card.value) if card.value.isdigit() else 0

        # Count points from AI hands
        for i, hand in enumerate(self.ai_hands):
            for card in hand:
                if card.value in ["+4", "Wild"]:
                    points += 50
                elif card.value in ["+2", "Skip", "Reverse"]:
                    points += 20
                else:
                    points += int(card.value) if card.value.isdigit() else 0

        # Add points to winner's score
        self.scores[winner] += points

    def game_won(self):
        """Handle player win condition"""
        win_frame = ctk.CTkFrame(self.game_frame, fg_color="#553D24")
        win_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(
            win_frame,
            text="You Won!",
            font=("Impact", 40)
        ).pack(pady=20)
        
        ctk.CTkButton(
            win_frame,
            text="Exit Game",
            font=("Arial", 20),
            command=lambda: self.game_frame.winfo_toplevel().destroy()
        ).pack(pady=20)

    def ai_won(self, ai_number):
        """Handle AI win condition"""
        win_frame = ctk.CTkFrame(self.game_frame, fg_color="#553D24")
        win_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(
            win_frame,
            text=f"AI {ai_number} Won!",
            font=("Impact", 40)
        ).pack(pady=20)
        
        ctk.CTkButton(
            win_frame,
            text="Exit Game",
            font=("Arial", 20),
            command=lambda: self.game_frame.winfo_toplevel().destroy()
        ).pack(pady=20)

    def add_rematch_button(self, frame):
        """Add rematch and quit buttons to win/lose screen"""
        buttons_frame = ctk.CTkFrame(frame, fg_color="transparent")
        buttons_frame.pack(pady=10)
        
        ctk.CTkButton(
            buttons_frame,
            text="Rematch",
            font=("Arial", 20),
            command=self.rematch
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            buttons_frame,
            text="Quit to Menu",
            font=("Arial", 20),
            command=lambda: self.quit_to_menu()
        ).pack(side="left", padx=10)
        
        # Show all scores
        scores_text = "\n".join([f"{player}: {score}" 
                                for player, score in self.scores.items()])
        ctk.CTkLabel(
            frame,
            text=f"\nTotal Scores:\n{scores_text}",
            font=("Arial", 20)
        ).pack(pady=10)

    def rematch(self):
        """Reset the game for a rematch"""
        # Clear hands
        self.player_hand.clear()
        self.ai_hands[0].clear()
        self.ai_hands[1].clear()
        self.discard_pile.clear()
        
        # Reset deck
        self.deck = self._create_deck()
        
        # Clear game frame
        for widget in self.game_frame.winfo_children():
            widget.destroy()
            
        # Reinitialize game
        self.initialize_game()

    def quit_to_menu(self):
        """Return to main menu"""
        from main import show_frame, home_frame
        show_frame(home_frame)