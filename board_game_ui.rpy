# This file contains all the Ren'Py screens for the board game UI.

# The main UI for the board game. It displays the board, pawns, and player info.
screen board_ui(players, current_player_name, turn_text):
    style_prefix "board"

    # Board Area (right side)
    frame:
        xalign 1.0
        yalign 0.5
        xmargin 50
        background None
        add "images/board_background.png"

        # Display player pawns on the board
        fixed:
            for p in players:
                # Get coordinates from the board_spaces list based on player's position
                $ pos_x, pos_y, _ = board_spaces[p.position]
                add p.pawn:
                    xpos pos_x
                    ypos pos_y

    # Player Info and Controls Panel (left side)
    vbox:
        yalign 0.5
        xpos 50  # FIXED: Changed 'xmargin 50' to the correct 'xpos 50'
        spacing 20

        text "Project Vitae" style "title"

        # Display player portraits and info
        for p in players:
            hbox:
                spacing 15
                imagebutton:
                    idle p.portrait
                    hover p.portrait
                    xysize (100, 100)
                    action Show("player_info_popup", player=p)

                vbox:
                    text p.name:
                        size 24
                        # Highlight the current player
                        if p.name == current_player_name:
                            color "#FFD700" # Gold
                    text "Position: [p.position]"

        text turn_text size 28 yalign 0.5

        # Show the "Roll Dice" button only when it's time to roll.
        if "Roll Dice" in turn_text:
            textbutton "Roll Dice" action Return("roll")

# A popup screen to show a player's detailed stats and active effects.
screen player_info_popup(player):
    modal True # This prevents interaction with other UI elements

    frame:
        xalign 0.5 yalign 0.5
        xsize 400
        padding (20, 20)
        vbox:
            xalign 0.5
            text player.name style "title" size 30
            null height 15

            if player.active_effects:
                text "Active Effects:"
                for effect in player.active_effects:
                    text "- [effect]"
            else:
                text "No active effects."

            null height 20
            textbutton "Close" action Hide("player_info_popup") xalign 0.5

# A screen to display a drawn card.
screen show_card(card):
    modal True
    frame:
        xalign 0.5 yalign 0.5
        padding (25, 25)
        vbox:
            spacing 10
            xalign 0.5
            text card["title"] size 32 bold True
            text card["description"] size 24
            null height 20
            textbutton "Continue" action Return() xalign 0.5

style board_frame is empty
style board_vbox is vbox
style board_text is text
style board_title is text
style board_textbutton is button
style board_textbutton_text is text

style board_text:
    font "DejaVuSans.ttf"
    size 20
    color "#FFFFFF"

style board_title:
    font "DejaVuSans.ttf"
    size 40
    color "#FFFFFF"
    xalign 0.5

style board_textbutton:
    xalign 0.5
    background Frame("gui/button/idle_background.png", 10, 10)
    hover_background Frame("gui/button/hover_background.png", 10, 10)

style board_textbutton_text:
    color "#FFFFFF"
    size 22
    xalign 0.5
    yalign 0.5