class Action:
    def __init__(self, trainer, action_type, detail, actor, target=None):
        self.trainer = trainer
        self.type = action_type
        self.detail = detail
        self.actor = actor
        self.target = target