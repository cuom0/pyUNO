class Card:
    def __init__(self, color, value):
        self.color = color   # ex. 'red', 'blue', 'green', 'yellow', 'jolly'
        self.value = value   # ex. '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+2', 'reverse', 'skip', 'wild', '+4'

    def __str__(self):
        return f"{self.color}_{self.value}"