class Move:
    """
    Represents a move (attack/status) in Gen 1.
    Based on the structure in 'data/moves/moves.asm'.
    """

    def __init__(self, move_id, name, effect, power, move_type, accuracy, max_pp):
        self.move_id = move_id
        self.name = name
        self.effect = effect  # ID of the move's secondary effect (e.g., POISON_SIDE_EFFECT1)
        self.power = power
        self.move_type = move_type  # e.g., 'NORMAL', 'FIRE'
        self.accuracy = accuracy  # 0 to 255 (255 is approx 99.6% due to the 255/256 bug)
        self.max_pp = max_pp
        self.current_pp = max_pp
