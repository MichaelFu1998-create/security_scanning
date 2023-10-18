def set_bot(self, bot):
        ''' Bot must be set before running '''
        self.bot = bot
        self.sink.set_bot(bot)