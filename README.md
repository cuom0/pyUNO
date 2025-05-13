# pyUNO

## Overview

pyUNO is a Python implementation of the popular card game UNO. It features a graphical user interface built with `customtkinter`, card images using `PIL`, and game logic that supports a single human player against two AI opponents.

## How to Play

1.  **Starting the Game:**
    * Launch the `main.py` script.
    * Click the "Play!" button on the home screen.
    * Select "Classic Mode" to begin a standard game of UNO.
2.  **Game Objective:**
    * The goal is to be the first player to get rid of all your cards.
3.  **Turns:**
    * Players take turns matching the top card of the discard pile by either color, number, or symbol.
    * If a player doesn't have a matching card, they must draw a card from the deck.
4.  **Card Types:**
    * **Number Cards (0-9):** Play a card with the same number or color.
    * **Skip:** Skips the next player's turn.
    * **Reverse:** Reverses the direction of play.
    * **+2:** Forces the next player to draw two cards and skips their turn.
    * **Wild:** The player chooses the color to continue play.
    * **+4 Wild:** The player chooses the color, and the next player draws four cards and is skipped.
5.  **Winning:**
    * The first player to have no cards left wins the game.
6.  **UNO Call:**
    * When a player has only one card left, they must click the "UNO!" button.
    * If they fail to do so and the next player plays a card, they incur a penalty of drawing two cards.
7.  **Game Interface:**
    * Your hand is displayed at the bottom. Click on a card to play it.
    * The top card of the discard pile is shown in the center-right.
    * The deck is in the center-left; click it to draw a card.
    * AI player information is displayed on the left and right.
    * A turn indicator shows whose turn it is.

## Code Explanation

The game is structured into three main Python files:

### 1. `card.py`

This file defines the `Card`, `Deck`, and `Game` classes, which handle the fundamental logic and data structures of the UNO game.

* **`Card` Class:**
    * `__init__(self, color, value)`: Initializes a card with a color (e.g., 'red', 'blue', 'black') and a value (e.g., '0', '5', '+2', 'wild'). It also sets the image path for the card.
    * `__str__(self)`: Returns a string representation of the card (e.g., "red\_5").
    * `get_image(self, size=(150, 225))` :  Returns a `CTkImage` object of the card, loaded from the image file. The `size` parameter allows resizing the image.
* **`Deck` Class:**
    * `__init__(self)`: Initializes an empty deck and calls `self.build()` to populate it.
    * `build(self)`: Creates all 108 cards of a standard UNO deck, including number cards, action cards, and wild cards.
    * `shuffle(self)`: Randomizes the order of the cards in the deck using `random.shuffle()`.
    * `draw(self)`: Removes and returns the top card from the deck (last card in the list). Returns `None` if the deck is empty.
* **`Game` Class:** (Note: This class is not directly used in the final application, its logic was moved to `GameManager`.)
    * `__init__(self, num_players=4)`: Initializes a new game with a specified number of players (default is 4). It creates a deck, shuffles it, deals initial hands, and sets up the discard pile.
    * `deal_initial_cards(self)`: Deals 7 cards to each player at the start of the game and places the first non-special card on the discard pile.
    * `is_valid_play(self, card)`: Checks if a card can be played on the current top card of the discard pile, considering color, value, and wild cards.
    * `play_card(self, player_idx, card_idx)`: Handles a player playing a card, removing it from their hand and placing it on the discard pile. It also calls `handle_special_card()` if necessary.
    * `handle_special_card(self, card)`: Implements the effects of special cards (+2, Reverse, Skip, +4).
    * `next_turn(self)`: Advances the game to the next player's turn, considering the direction of play.

### 2. `game_manager.py`

This file contains the `GameManager` class, which orchestrates the game logic, manages the UI updates, and handles player and AI interactions.

* **`GameManager` Class:**
    * `__init__(self, game_frame, ui_elements)`: Initializes the game manager with references to the game's UI frame (`game_frame`) and a dictionary of UI elements (`ui_elements`). It also sets up initial game state variables.
    * `_create_deck(self)`:  (Private method) Creates and shuffles the UNO deck, similar to `Deck.build()` in `card.py`.
    * `initialize_game(self)`: Deals the initial 7 cards to each player (including AI players) and sets the first card of the discard pile.
    * `handle_wild_card(self, card)`:  Presents a color selection popup when a wild card is played.
    * `complete_wild_card_play(self, card, chosen_color, popup, win_pending=False)`:  Finalizes the play of a wild card after a color is selected, updates the game state, and handles the next turn.
    * `is_valid_play(self, card)`: Checks if a card can be legally played on the discard pile.
    * `update_game_state(self)`: Updates all UI elements to reflect the current game state (player hand, discard pile, AI hand counts, turn indicator, UNO button state).
    * `play_card(self, card)`: Handles the player's card play, including UNO call checks, win conditions, and wild card handling.
    * `update_player_hand(self)`:  Updates the display of the player's hand with `CTkButton`s for each card.
    * `update_ai_labels(self)`: Updates the labels showing the number of cards held by each AI player.
    * `draw_card(self)`: Allows the player to draw a card from the deck.
    * `call_uno(self)`: Handles the player's "UNO" call.
    * `handle_special_card(self, card)`: Implements the actions of special cards (+2, Skip, Reverse, +4).
    * `handle_ai_turn(self)`: Controls the AI players' turns, including card selection, playing cards, drawing cards, and handling special cards.
    * `calculate_score(self, winner)`: Calculates the score for the winner based on the cards left in the other players' hands.
    * `game_won(self)`:  Displays a "You Won!" screen.
    * `ai_won(self, ai_number)`: Displays an "AI X Won!" screen.
    * `add_rematch_button(self, frame)`: Adds rematch and quit buttons to the win/lose screens.
    * `rematch(self)`: Resets the game for a new round.
    * `quit_to_menu(self)`: Returns to the main menu.

### 3. `main.py`

This file is the entry point of the game. It sets up the main application window, manages the different frames (home screen, credits, game mode selection, and the game itself), and initializes the game.

* **Global Setup:**
    * Initializes the main application window (`homescreen`) using `customtkinter`.
    * Sets window properties (size, theme, resizability, color, title).
* **`show_frame(frame)` Function:**
    * Raises the specified frame to the top, making it visible.
* **`close_program()` Function:**
    * Closes the main application window.
* **`start_game()` Function:**
    * Creates the game frame.
    * Initializes the UI elements (card holder, UNO button, deck display, discard pile display, turn indicator, AI labels).
    * Creates an instance of the `GameManager` class.
    * Binds the deck label to the `draw_card` method of the `GameManager`.
    * Calls `game_manager.initialize_game()` to start the game.
* **`open_github()` Function:**
    * Opens the developer's GitHub profile in a web browser.
* **Frame Definitions:**
    * **`home_frame`:** The main menu with buttons to play, view credits, and exit.
    * **`credit_frame`:** Displays credits information and a link to the developer's GitHub.
    * **`mode_selector`:** Allows the player to select the game mode (currently only "Classic Mode" is implemented).
* **Button Event Handling:**
    * Each button is associated with a command that calls a function to switch frames, start the game, or exit.
* **Frame Visibility:**
    * The `home_frame` is initially raised to be the first screen the user sees.
* **Main Loop:**
    * `homescreen.mainloop()` starts the `customtkinter` event loop, which listens for user interactions and updates the GUI.

## Additional Notes

* The code uses `customtkinter` for the graphical interface, providing a modern look with theming capabilities.
* Card images are loaded using `PIL` (Pillow) and displayed using `customtkinter`'s image handling.
* The game logic is separated from the UI management, making the code more organized and maintainable.
* AI opponents are implemented with basic card-playing logic.
* Error handling (using `try-except` blocks) is included in some parts of the code to prevent crashes.
* The code is well-commented, explaining the purpose of different functions and sections.
