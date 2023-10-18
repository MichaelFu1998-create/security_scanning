def do_fullscreen(self, line):
        """
        Make the current window fullscreen
        """
        self.bot.canvas.sink.trigger_fullscreen_action(True)
        print(self.response_prompt, file=self.stdout)