async def _playat(self, ctx, index: int):
        """ Plays the queue from a specific point. Disregards tracks before the index. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if index < 1:
            return await ctx.send('Invalid specified index.')

        if len(player.queue) < index:
            return await ctx.send('This index exceeds the queue\'s length.')

        await player.play_at(index-1)