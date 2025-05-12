import random
from PIL import Image
import customtkinter as ctk

class Card:
    def __init__(self, color, value):
        self.color = color   # ex. 'red', 'blue', 'green', 'yellow', 'jolly'
        self.value = value   # ex. '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+2', 'reverse', 'skip', 'wild', '+4'
        self.image_path = f"./media/cards/{color}_{value}.png"
        
    def __str__(self):
        return f"{self.color}_{self.value}"
    
    def get_image(self, size=(150, 225)):
        return ctk.CTkImage(
            light_image=Image.open(self.image_path),
            dark_image=Image.open(self.image_path),
            size=size
        )

class Deck:
    def __init__(self):
        self.cards = []
        self.build()
        
    def build(self):
        colors = ['red', 'blue', 'green', 'yellow']
        numbers = [str(n) for n in range(10)]
        actions = ['+2', 'reverse', 'skip']
        
        # Add number cards (0-9)
        for color in colors:
            self.cards.append(Card(color, '0'))  # One zero per color
            for num in numbers[1:]:  # Two of each 1-9
                self.cards.extend([Card(color, num) for _ in range(2)])
                
        # Add action cards (two of each per color)
        for color in colors:
            for action in actions:
                self.cards.extend([Card(color, action) for _ in range(2)])
                
        # Add wild cards
        for _ in range(4):
            self.cards.append(Card('black', 'wild'))
            self.cards.append(Card('black', '+4'))
            
    def shuffle(self):
        random.shuffle(self.cards)
        
    def draw(self):
        if not self.cards:
            return None
        return self.cards.pop()

class Game:
    def __init__(self, num_players=4):
        self.deck = Deck()
        self.deck.shuffle()
        self.players = [[] for _ in range(num_players)]
        self.current_player = 0
        self.direction = 1  # 1 for clockwise, -1 for counter-clockwise
        self.discard_pile = []
        self.deal_initial_cards()
        
    def deal_initial_cards(self):
        # Deal 7 cards to ALL players (including human player)
        for _ in range(7):
            for player in self.players:
                card = self.deck.draw()
                if card:
                    player.append(card)
                    
        # Draw first card for discard pile (skip special cards)
        while True:
            card = self.deck.draw()
            if card and card.color != 'black' and card.value not in ['+2', '+4', 'reverse', 'skip']:
                self.discard_pile.append(card)
                break
            elif card:
                self.deck.cards.append(card)  # Put special card back in deck
                self.deck.shuffle()
        
    def is_valid_play(self, card):
        top_card = self.discard_pile[-1]
        return (card.color == top_card.color or 
                card.value == top_card.value or 
                card.color == 'black')
    
    def play_card(self, player_idx, card_idx):
        if player_idx != self.current_player:
            return False
            
        card = self.players[player_idx][card_idx]
        if not self.is_valid_play(card):
            return False
            
        self.discard_pile.append(self.players[player_idx].pop(card_idx))
        self.handle_special_card(card)
        return True
        
    def handle_special_card(self, card):
        if card.value == 'reverse':
            self.direction *= -1
        elif card.value == 'skip':
            self.next_turn()
        elif card.value == '+2':
            next_player = (self.current_player + self.direction) % len(self.players)
            for _ in range(2):
                self.players[next_player].append(self.deck.draw())
        elif card.value == '+4':
            next_player = (self.current_player + self.direction) % len(self.players)
            for _ in range(4):
                self.players[next_player].append(self.deck.draw())
                
        self.next_turn()
        
    def next_turn(self):
        self.current_player = (self.current_player + self.direction) % len(self.players)