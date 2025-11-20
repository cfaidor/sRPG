# This file contains the data for all cards in the game.
# This approach makes it easy to add, remove, or modify cards without
# changing the core game logic.

init python:
    card_decks = {
        "green": [
            # Positive Effects
            {"title": "Sudden Burst", "description": "Move forward 2 extra spaces.", "effect": "move_spaces", "value": 2},
            {"title": "Good Fortune", "description": "Move forward 3 extra spaces.", "effect": "move_spaces", "value": 3},
            {"title": "Feeling Lucky", "description": "On your next turn, roll two dice.", "effect": "apply_status", "value": "roll_2d6"},
        ],
        "red": [
            # Negative Effects
            {"title": "Stumble", "description": "Move back 2 spaces.", "effect": "move_spaces", "value": -2},
            {"title": "Exhaustion", "description": "Miss your next turn.", "effect": "apply_status", "value": "miss_turn"},
            {"title": "Wrong Turn", "description": "Move back 1 space.", "effect": "move_spaces", "value": -1},
        ],
        "blue": [
            # Punishment Effects
            {"title": "Total Recall", "description": "Go back to the start.", "effect": "go_to_start", "value": None},
            {"title": "Misfortune", "description": "Move back 5 spaces.", "effect": "move_spaces", "value": -5},
            {"title": "Amnesia", "description": "Lose all your active positive effects.", "effect": "clear_positive_effects", "value": None},
        ],
        "purple": [
            # Player vs. Player Effects
            {"title": "Envy", "description": "Swap places with the player currently in the lead.", "effect": "swap_with_leader", "value": None},
            {"title": "Targeted Push", "description": "Choose another player to move back 3 spaces.", "effect": "push_player_back", "value": 3},
            {"title": "Theft of Luck", "description": "Steal a positive effect from another player.", "effect": "steal_effect", "value": None},
        ]
    }

    # Define which status effects are considered "positive" for cards like "Amnesia"
    positive_effects = ["roll_2d6"]