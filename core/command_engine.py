class CommandEngine:
    def __init__(self, commands):
        self.commands = commands

    def build(self, intent, params):
        if intent not in self.commands:
            return None
        cmd = self.commands[intent]
        for k, v in params.items():
            cmd = cmd.replace("{" + k + "}", str(v))
        return cmd
