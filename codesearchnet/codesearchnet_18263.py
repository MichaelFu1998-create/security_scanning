def whoami(self, msg, args):
        """Prints information about the user and bot version."""
        output = ["Hello %s" % msg.user]
        if hasattr(self._bot.dispatcher, 'auth_manager') and msg.user.is_admin is True:
            output.append("You are a *bot admin*.")
        output.append("Bot version: %s-%s" % (self._bot.version, self._bot.commit))
        return '\n'.join(output)