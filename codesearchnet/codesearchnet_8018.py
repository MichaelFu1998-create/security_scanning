def register_hook(self, func):
        """
        Registers a hook. Since this probably is a bit difficult, I'll explain it in detail.
        A hook basically is an object of a function you pass. This will append that object to a list and whenever
        an event from the Lavalink server is dispatched, the function will be called internally. For declaring the
        function that should become a hook, pass ``event` as its sole parameter.
        Can be a function but also a coroutine.

        Example for a method declaration inside a class:
        ---------------
            self.bot.lavalink.register_hook(my_hook)

            async def my_hook(self, event):
                channel = self.bot.get_channel(event.player.fetch('channel'))
                if not channel:
                    return

                if isinstance(event, lavalink.Events.TrackStartEvent):
                    await channel.send(embed=discord.Embed(title='Now playing:',
                                                           description=event.track.title,
                                                           color=discord.Color.blurple()))
        ---------------
        :param func:
            The function that should be registered as a hook.
        """

        if func not in self.hooks:
            self.hooks.append(func)