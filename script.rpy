# The script of the game.

# Declare characters used by this game.
define e = Character("Eileen")

# The game starts here.
label start:

    # This is where your main visual novel story would go.
    scene black
    with fade

    e "Welcome to Project Vitae."
    e "Tonight, four souls will compete on the board of life."
    e "Let's begin Night 1."

    # This is the call to the board game.
    # You can configure the number of rounds for the session.
    call board_game(rounds=3)

    # The board_game label returns a value in _return.
    # We can use this to see who won.
    if _return == "limit_reached":
        e "The night ends. No one has reached the center."
        e "The story continues..."
    else:
        e "We have a winner! Congratulations, [_return]!"
        e "Now, let's see what destiny has in store for you..."

    # The game continues here after the board game is over.
    e "And so, a new chapter begins."

    return