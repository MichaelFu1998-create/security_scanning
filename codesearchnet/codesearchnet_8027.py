async def _previous(self, ctx):
        """ Plays the previous song. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        try:
            await player.play_previous()
        except lavalink.NoPreviousTrack:
            await ctx.send('There is no previous song to play.')