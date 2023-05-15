class CommandNode:
    def __init__(self, command, prev=None):
        self.command = command
        self.prev = prev

class CommandHistory:
    def __init__(self):
        self.history = {}

    def add_command(self, user_id, command):
        if user_id not in self.history:
            self.history[user_id] = CommandNode(command)
        else:
            self.history[user_id] = CommandNode(command, self.history[user_id])

    def get_last_command(self, user_id):
        if user_id not in self.history:
            return None
        return self.history[user_id].command

    def get_all_commands(self, user_id):
        if user_id not in self.history:
            return []
        commands = []
        node = self.history[user_id]
        while node:
            commands.append(node.command)
            node = node.prev
        return commands

    def get_previous_command(self, user_id):
        if user_id not in self.history:
            return None
        if not self.history[user_id].prev:
            return self.history[user_id].command
        self.history[user_id] = self.history[user_id].prev
        return self.history[user_id].command

    def get_next_command(self, user_id):
        if user_id not in self.history:
            return None
        if not self.history[user_id].prev:
            return self.history[user_id].command
        if not self.history[user_id].prev.prev:
            return self.history[user_id].prev.command
        self.history[user_id] = self.history[user_id].prev
        return self.history[user_id].command

    def clear_history(self, user_id):
        if user_id in self.history:
            self.history[user_id] = None
