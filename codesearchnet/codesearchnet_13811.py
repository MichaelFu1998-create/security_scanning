def do_windowed(self, line):
        """
        Un-fullscreen the current window
        """
        self.bot.canvas.sink.trigger_fullscreen_action(False)
        print(self.response_prompt, file=self.stdout)