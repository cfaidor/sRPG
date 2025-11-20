# This file contains the main logic for the board game.

# Define the coordinates for each space on the board.
# Format: (x_coordinate, y_coordinate, deck_color)
# You must define these based on your board image.
# The LAST entry is the goal space.
default board_spaces = [
    # Outer Ring
    (50, 50, "green"), (150, 50, "red"), (250, 50, "blue"), (350, 50, "purple"),
    (450, 50, "green"), (550, 50, "red"), (650, 50, "blue"), (750, 50, "purple"),
    (850, 50, "green"), (950, 50, "red"), (1050, 50, "blue"), (1150, 50, "purple"),
    (1250, 50, "green"), (1250, 150, "red"), (1250, 250, "blue"), (1250, 350, "purple"),
    (1250, 450, "green"), (1250, 550, "red"), (1250, 650, "blue"),
    # ...and so on, spiraling inwards...
    # For this example, we'll create a short path.
    (1150, 650, "purple"), (1050, 650, "green"), (950, 650, "red"), (850, 650, "blue"),
    (750, 650, "purple"), (650, 650, "green"), (550, 650, "red"), (450, 650, "blue"),
    (350, 650, "purple"), (250, 650, "green"), (150, 650, "red"), (50, 650, "blue"),
    (50, 550, "purple"), (50, 450, "green"), (50, 350, "red"), (50, 250, "blue"), (50, 150, "purple"),
    # Inner Ring
    (150, 150, "green"), (250, 150, "red"), (350, 150, "blue"),
    (450, 150, "purple"), (550, 150, "green"), (650, 150, "red"),
    (750, 150, "blue"), (850, 150, "purple"), (950, 150, "green"),
    # Goal Space (Must be the last one)
    (650, 350, "goal")
]

# The main label that runs the board game.
label board_game(rounds=1):
    python:
        # --- 1. SETUP ---

        # Define the Player class to hold all player-specific data
        class Player:
            def __init__(self, name, pawn_img, portrait_img):
                self.name = name
                self.pawn = pawn_img
                self.portrait = portrait_img
                self.position = 0
                self.active_effects = [] # This is the effect "backlog"

        # Initialize the four players
        players = [
            Player("John", "images/pawn_john.png", "images/portrait_john.png"),
            Player("Emily", "images/pawn_emily.png", "images/portrait_emily.png"),
            Player("Brad", "images/pawn_brad.png", "images/portrait_brad.png"),
            Player("Sarah", "images/pawn_sarah.png", "images/portrait_sarah.png")
        ]

        current_round = 1
        game_over = False
        winner = None
        goal_position = len(board_spaces) - 1

        # --- 2. MAIN GAME LOOP ---
        while not game_over:
            renpy.say(None, "Round {} of {} begins.".format(current_round, rounds), interact=False)
            renpy.pause(1.5)

            # Iterate through each player for their turn
            for current_player in players:
                if game_over:
                    break

                turn_text = "It's {}'s turn.".format(current_player.name)
                renpy.show_screen("board_ui", players=players, current_player_name=current_player.name, turn_text=turn_text)
                renpy.restart_interaction()

                # --- Check for Status Effects ---
                if "miss_turn" in current_player.active_effects:
                    current_player.active_effects.remove("miss_turn")
                    renpy.say(None, "{} misses their turn!".format(current_player.name))
                    renpy.pause(1.5)
                    continue # Skip to the next player's turn

                # --- Dice Roll ---
                roll_2d6 = "roll_2d6" in current_player.active_effects
                if roll_2d6:
                    current_player.active_effects.remove("roll_2d6")

                turn_text = "{} is about to roll... (Click 'Roll Dice')".format(current_player.name)
                renpy.show_screen("board_ui", players=players, current_player_name=current_player.name, turn_text=turn_text)

                ui.interact()

                if roll_2d6:
                    dice_roll = renpy.random.randint(1, 6) + renpy.random.randint(1, 6)
                    renpy.say(None, "{} is rolling 2D6... and gets a {}!".format(current_player.name, dice_roll))
                else:
                    dice_roll = renpy.random.randint(1, 6)
                    renpy.say(None, "{} rolls a {}!".format(current_player.name, dice_roll))
                renpy.pause(1.0)

                # --- Movement ---
                new_position = current_player.position + dice_roll
                current_player.position = min(new_position, goal_position)

                turn_text = "{} moves to space {}.".format(current_player.name, current_player.position + 1)
                renpy.show_screen("board_ui", players=players, current_player_name=current_player.name, turn_text=turn_text)
                renpy.pause(1.5)

                # --- Check for Win Condition ---
                if current_player.position >= goal_position:
                    game_over = True
                    winner = current_player.name
                    renpy.say(None, "{} has reached the center! They are the winner!".format(winner))
                    renpy.pause(2.0)
                    break

                # --- Resolve Space/Card Effect ---
                space_x, space_y, deck_type = board_spaces[current_player.position]

                # FIXED: Added 'store.' to access the global card_decks variable
                if deck_type in store.card_decks:
                    renpy.say(None, "{} landed on a {} space and draws a card...".format(current_player.name, deck_type))
                    renpy.pause(1.0)

                    # FIXED: Added 'store.' here as well
                    drawn_card = renpy.random.choice(store.card_decks[deck_type])
                    renpy.call_screen("show_card", card=drawn_card)

                    # FIXED: Added 'store.' to access the global effect_function_map
                    effect_func = store.effect_function_map.get(drawn_card['effect'])
                    if effect_func:
                        # We also need to pass the 'positive_effects' list to the functions that need it
                        if drawn_card['effect'] in ["clear_positive_effects", "steal_effect"]:
                             effect_func(current_player, players, drawn_card['value'], store.positive_effects)
                        else:
                             effect_func(current_player, players, drawn_card['value'])

                    current_player.position = min(max(0, current_player.position), goal_position)
                    renpy.pause(1.5)

            # --- End of Round ---
            if game_over:
                break

            current_round += 1
            if current_round > rounds:
                game_over = True
                winner = "limit_reached"
                renpy.say(None, "The round limit has been reached! The game is over.")
                renpy.pause(2.0)

    hide screen board_ui
    return winner