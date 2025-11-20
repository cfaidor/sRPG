# This file contains the Python functions that execute card effects.
# Keeping the logic separate makes the system clean and modular.

init python:
    # --- UTILITY FUNCTIONS ---
    def get_leader(players, current_player):
        leader = None
        max_pos = -1
        for p in players:
            if p != current_player and p.position > max_pos:
                max_pos = p.position
                leader = p
        return leader

    # --- CARD EFFECT FUNCTIONS ---
    # Note: Some functions now accept 'positive_effects_list' to know which effects are good.
    def effect_move_spaces(player, players, value):
        renpy.say(None, "{} moves {} spaces.".format(player.name, value))
        player.position = max(0, player.position + value)

    def effect_apply_status(player, players, value):
        renpy.say(None, "{} gains the '{}' effect.".format(player.name, value))
        player.active_effects.append(value)

    def effect_go_to_start(player, players, value):
        renpy.say(None, "{} goes back to the start!".format(player.name))
        player.position = 0

    def effect_clear_positive_effects(player, players, value, positive_effects_list):
        renpy.say(None, "{} loses all positive effects.".format(player.name))
        player.active_effects = [eff for eff in player.active_effects if eff not in positive_effects_list]

    def effect_swap_with_leader(player, players, value):
        leader = get_leader(players, player)
        if leader:
            renpy.say(None, "{} swaps places with {}!".format(player.name, leader.name))
            player.position, leader.position = leader.position, player.position
        else:
            renpy.say(None, "There is no one ahead to swap with.")

    def effect_push_player_back(player, players, value):
        targets = [p for p in players if p != player]
        if not targets:
            renpy.say(None, "There's no one else to target.")
            return

        menu_choices = [(p.name, p) for p in targets]
        chosen_player = renpy.display_menu(menu_choices)

        renpy.say(None, "{} pushes {} back {} spaces.".format(player.name, chosen_player.name, value))
        chosen_player.position = max(0, chosen_player.position - value)

    def effect_steal_effect(player, players, value, positive_effects_list):
        targets = [p for p in players if p != player and any(eff in positive_effects_list for eff in p.active_effects)]
        if not targets:
            renpy.say(None, "No other player has a positive effect to steal.")
            return

        victim_choices = [(p.name, p) for p in targets]
        victim = renpy.display_menu(victim_choices)

        stealable_effects = [eff for eff in victim.active_effects if eff in positive_effects_list]
        if not stealable_effects:
             renpy.say(None, "{} has no positive effects left to steal.".format(victim.name))
             return

        effect_choices = [(eff, eff) for eff in stealable_effects]
        chosen_effect = renpy.display_menu(effect_choices)

        renpy.say(None, "{} steals the '{}' effect from {}!".format(player.name, chosen_effect, victim.name))
        victim.active_effects.remove(chosen_effect)
        player.active_effects.append(chosen_effect)


    # This dictionary maps the effect string from card_definitions.rpy to the actual function here.
    effect_function_map = {
        "move_spaces": effect_move_spaces,
        "apply_status": effect_apply_status,
        "go_to_start": effect_go_to_start,
        "clear_positive_effects": effect_clear_positive_effects,
        "swap_with_leader": effect_swap_with_leader,
        "push_player_back": effect_push_player_back,
        "steal_effect": effect_steal_effect
    }