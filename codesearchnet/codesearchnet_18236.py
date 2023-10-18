def push(self, message):
        """
        Takes a SlackEvent, parses it for a command, and runs against registered plugin
        """
        if self._ignore_event(message):
            return None, None
        args = self._parse_message(message)
        self.log.debug("Searching for command using chunks: %s", args)
        cmd, msg_args = self._find_longest_prefix_command(args)
        if cmd is not None:
            if message.user is None:
                self.log.debug("Discarded message with no originating user: %s", message)
                return None, None
            sender = message.user.username
            if message.channel is not None:
                sender = "#%s/%s" % (message.channel.name, sender)
            self.log.info("Received from %s: %s, args %s", sender, cmd, msg_args)
            f = self._get_command(cmd, message.user)
            if f:
                if self._is_channel_ignored(f, message.channel):
                    self.log.info("Channel %s is ignored, discarding command %s", message.channel, cmd)
                    return '_ignored_', ""
                return cmd, f.execute(message, msg_args)
            return '_unauthorized_', "Sorry, you are not authorized to run %s" % cmd
        return None, None