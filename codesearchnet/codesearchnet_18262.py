def shutdown(self, msg, args):
        """Causes the bot to gracefully shutdown."""
        self.log.info("Received shutdown from %s", msg.user.username)
        self._bot.runnable = False
        return "Shutting down..."