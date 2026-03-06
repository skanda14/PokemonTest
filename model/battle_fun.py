

def get_general_stage_multiplier(n):
    numerator, denominator = 2,2
    if n>0:
        numerator += n
    elif n<0:
        denominator += abs(n)
    return numerator/denominator


def who_has_highest_calculated_speed(action_a, action_b):
    pokemon_a = action_a.actor
    pokemon_b = action_b.actor
    calculated_speed_a = pokemon_a.stats["speed"] * get_general_stage_multiplier(
        pokemon_a.stat_stages["speed"])
    calculated_speed_b = pokemon_b.stats["speed"] * get_general_stage_multiplier(
        pokemon_b.stat_stages["speed"])
    if calculated_speed_a > calculated_speed_b:
        return action_a, action_b
    elif calculated_speed_a < calculated_speed_b:
        return action_b, action_a
    else:
        return None


def who_has_highest_move_priority(action_a, action_b):
    if action_a.detail.priority > action_b.detail.priority:
        return action_a, action_b
    elif action_a.detail.priority < action_b.detail.priority:
        return action_b, action_a
    else:
        return None

def who_has_highest_action_type_priority(action_a, action_b, action_run, action_switch, action_item):
    if action_a.type == action_run:
        return action_a, action_b
    elif action_b.type == action_run:
        return action_b, action_a

    if action_a.type == action_switch:
        return action_a, action_b
    elif action_b.type == action_switch:
        return action_b, action_a

    if action_a.type == action_item:
        return action_a, action_b
    elif action_b.type == action_item:
        return action_b, action_a

    return None

