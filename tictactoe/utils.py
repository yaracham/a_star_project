from state import x_player, o_player

computer_player = x_player
human_player = o_player

min_util = -1000
max_util = +1000

def other_player(player):
    if player == x_player:
        return o_player
    else:
        return x_player
    

def PLAYER_UTIL(player):
    if player == computer_player:
        return max_util
    elif player == human_player:
        return min_util
    return 0

