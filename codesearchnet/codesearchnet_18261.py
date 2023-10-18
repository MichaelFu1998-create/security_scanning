def save(self, msg, args):
        """Causes the bot to write its current state to backend."""
        self.send_message(msg.channel, "Saving current state...")
        self._bot.plugins.save_state()
        self.send_message(msg.channel, "Done.")