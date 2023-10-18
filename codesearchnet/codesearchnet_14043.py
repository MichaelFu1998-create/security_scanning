def schedule_snapshot(self, format):
        """
        Tell the canvas to perform a snapshot when it's finished rendering
        :param format:
        :return:
        """
        bot = self.bot
        canvas = self.bot.canvas
        script = bot._namespace['__file__']
        if script:
            filename = os.path.splitext(script)[0] + '.' + format
        else:
            filename = 'output.' + format

        f = canvas.output_closure(filename, self.bot._frame)
        self.scheduled_snapshots.append(f)