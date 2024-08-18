def push_game_mode(game_state, mode):
    game_state.mode.append(mode)

def pop_game_mode(game_state):
    return game_state.mode.pop()

def peek_game_mode(game_state):
    return game_state.mode[-1] if len(game_state.mode) > 0 else None