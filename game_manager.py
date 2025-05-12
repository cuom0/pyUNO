import customtkinter as ctk
from card import Game, Card
import random

class GameManager:
    def __init__(self, game_frame, ui_elements):
        self.game_frame = game_frame
        self.ui_elements = ui_elements
        self.game = Game(4)
        self.card_buttons = []
        self.color_frame = None
        self.uno_called = False
        
        # Setup initial game state
        self.setup_color_selector()
        self.setup_deck_click()
        self.update_game_state()

    def setup_color_selector(self):
        """Create and configure the color selection frame"""
        self.color_frame = ctk.CTkFrame(self.game_frame, fg_color="#333333")

        # Add title label
        ctk.CTkLabel(
            self.color_frame,
            text="Choose a color:",
            font=("Arial", 24),
            text_color="white"
        ).pack(pady=10)

        # Create color buttons
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

        # Hide initially
        self.color_frame.place_forget()

    def handle_color_selection(self, color):
        """Handle color selection for wild cards"""
        if self.color_frame:
            self.color_frame.place_forget()
            if self.game.discard_pile:
                self.game.discard_pile[-1].color = color
                self.game.next_turn()
                self.ai_turns()
                self.update_game_state()

    def show_color_selector(self):
        """Display the color selector in the center of the screen"""
        if self.color_frame:
            self.color_frame.place(relx=0.5, rely=0.5, anchor="center")

    def setup_deck_click(self):
        """Setup deck click handler"""
        if 'deck_label' in self.ui_elements:
            self.ui_elements['deck_label'].configure(cursor="hand2")
            self.ui_elements['deck_label'].bind("<Button-1>", self.on_deck_click)

    def on_deck_click(self, event):
        """Handle deck click event"""
        try:
            self.draw_card()
        except Exception as e:
            print(f"Error drawing card: {e}")

    def update_game_state(self):
        """Update all UI elements safely"""
        try:
            # Update last card
            if self.game.discard_pile:
                top_card = self.game.discard_pile[-1]
                self.ui_elements['last_card'].configure(image=top_card.get_image())

            # Update player hand
            if self.card_holder:
                self.update_player_hand()

            # Update AI info
            self.update_ai_info()

            # Check for UNO condition when it's player's turn
            if (self.game.current_player == 0 and
                len(self.game.players[0]) == 2 and
                not self.uno_called):
                self.ui_elements['uno_button'].configure(state="normal")
            else:
                self.ui_elements['uno_button'].configure(state="disabled")

        except Exception as e:
            print(f"Error updating game state: {e}")

    def update_player_hand(self):
        """Update player's hand display"""
        if 'card_holder' in self.ui_elements:
            card_holder = self.ui_elements['card_holder']
            # Clear existing cards
            for widget in card_holder.winfo_children():
                widget.destroy()

            # Add cards to hand
            for card in self.game.players[0]:
                card_btn = ctk.CTkButton(
                    card_holder,
                    image=card.get_image((100, 150)),
                    text="",
                    width=100,
                    command=lambda c=card: self.play_card(c)
                )
                card_btn.pack(side="left", padx=5)

    def update_ai_info(self):
        """Update AI labels with current card counts"""
        if 'ai1_label' in self.ui_elements:
            self.ui_elements['ai1_label'].configure(
                text=f"AI 1\n{len(self.game.players[1])} Cards"
            )
        if 'ai2_label' in self.ui_elements:
            self.ui_elements['ai2_label'].configure(
                text=f"AI 2\n{len(self.game.players[2])} Cards"
            )

    def draw_card(self):
        """Handle drawing a card from the deck"""
        if self.game.current_player == 0:  # Only allow drawing on player's turn
            drawn_card = self.game.deck.draw()
            if drawn_card:
                # Add card to player's hand
                self.game.players[0].append(drawn_card)
                self.update_player_hand()

                # Check if drawn card is playable
                top_card = self.game.discard_pile[-1]
                if not (drawn_card.color == top_card.color or
                       drawn_card.value == top_card.value or
                       drawn_card.color == 'black'):
                    # Card not playable, end turn
                    self.game.next_turn()
                    self.game_frame.after(500, self.ai_turns)

    def play_card(self, card):
        if self.game.current_player == 0:
            try:
                player_hand = self.game.players[0]
                card_idx = player_hand.index(card)

                if self.game.is_valid_play(card):
                    # Play the card
                    self.game.discard_pile.append(player_hand.pop(card_idx))

                    # Check if UNO wasn't called when playing second-to-last card
                    if len(player_hand) == 1 and not self.uno_called:
                        self.show_uno_warning()
                        # Add 2 cards as punishment
                        for _ in range(2):
                            drawn = self.game.deck.draw()
                            if drawn:
                                player_hand.append(drawn)

                    # Handle special cards and continue game
                    if card.color == 'black':
                        self.show_color_selector()
                    else:
                        self.game.next_turn()
                        self.update_game_state()
                        self.game_frame.after(1000, self.ai_turns)

            except Exception as e:
                print(f"Error playing card: {e}")

    def show_uno_warning(self):
        warning_frame = ctk.CTkFrame(self.game_frame, fg_color="#333333")
        warning_frame.place(relx=0.5, rely=0.5, anchor="center")

        warning_label = ctk.CTkLabel(
            warning_frame,
            text="Forgot to yell UNO!\n+2 cards",
            font=("Arial", 24),
            text_color="white"
        )
        warning_label.pack(pady=20, padx=40)

        # Remove warning after 2 seconds
        self.game_frame.after(2000, warning_frame.destroy)

    def call_uno(self):
        self.uno_called = True
        self.ui_elements['uno_button'].configure(state="disabled")

    def ai_turns(self):
        """Handle AI turns"""
        if self.game.current_player == 0:  # Skip if it's player's turn
            return

        try:
            self.ui_elements['turn_label'].configure(text="AI's Turn")

            # Process single AI turn
            ai_idx = self.game.current_player
            ai_hand = self.game.players[ai_idx]

            # AI logic
            played = False
            for card_idx, card in enumerate(ai_hand):
                if self.game.is_valid_play(card):
                    # Remove card from AI hand and add to discard pile
                    played_card = ai_hand.pop(card_idx)
                    self.game.discard_pile.append(played_card)
                    played = True

                    # Check for win immediately after playing card
                    if len(ai_hand) == 0:
                        self.check_win()
                        return  # Stop game if AI won

                    # Handle AI wild card
                    if card.color == 'black':
                        colors = ["red", "blue", "green", "yellow"]
                        chosen_color = random.choice(colors)
                        self.game.discard_pile[-1].color = chosen_color
                        self.show_ai_color_choice(chosen_color)
                    break

            if not played:
                # AI draws a card if can't play
                drawn_card = self.game.deck.draw()
                if drawn_card:
                    ai_hand.append(drawn_card)

            # Update game state
            self.game.next_turn()
            self.update_game_state()

            # Schedule next AI turn or return to player
            if self.game.current_player != 0 and not self.check_win():
                self.game_frame.after(1000, self.ai_turns)
            else:
                self.ui_elements['turn_label'].configure(text="Your Turn")

        except Exception as e:
            print(f"Error during AI turns: {e}")
            self.ui_elements['turn_label'].configure(text="Your Turn")
            self.game.current_player = 0  # Reset to player's turn if error occurs

    def show_ai_color_choice(self, color):
        """Show temporary notification of AI color choice"""
        notification = ctk.CTkLabel(
            self.game_frame,
            text=f"AI chose {color}!",
            font=("Arial", 24),
            fg_color="black",
            text_color="white"
        )
        notification.place(relx=0.5, rely=0.3, anchor="center")
        self.game_frame.after(2000, notification.destroy)  # Remove after 2 seconds

    def check_win(self):
        """Check for win condition and show win screen if game is over"""
        for i, hand in enumerate(self.game.players):
            if len(hand) == 0:
                winner = "You" if i == 0 else f"AI {i}"
                self.show_win_screen(winner)
                return True
        return False

    def show_win_screen(self, winner):
        win_frame = ctk.CTkFrame(self.game_frame, fg_color="#092c4d")
        win_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Win message
        ctk.CTkLabel(
            win_frame,
            text=f"{winner} won the game!",
            font=("Impact", 40),
            text_color="white"
        ).pack(pady=20)
        
        # Play again button
        ctk.CTkButton(
            win_frame,
            text="Play Again",
            font=("Arial", 24),
            command=lambda: [win_frame.destroy(), self.restart_game()]
        ).pack(pady=10)
        
        # Quit button
        ctk.CTkButton(
            win_frame,
            text="Quit",
            font=("Arial", 24),
            command=lambda: [win_frame.destroy(), self.quit_game()]
        ).pack(pady=10)

    def restart_game(self):
        self.game = Game(4)
        self.uno_called = False
        self.ui_elements['uno_button'].configure(state="disabled")
        self.update_game_state()

    def quit_game(self):
        from main import show_frame, home_frame
        show_frame(home_frame)