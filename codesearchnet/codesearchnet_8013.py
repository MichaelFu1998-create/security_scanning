async def _play(self, ctx, *, query: str):
        """ Searches and plays a song from a given query. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        query = query.strip('<>')

        if not url_rx.match(query):
            query = f'ytsearch:{query}'

        tracks = await self.bot.lavalink.get_tracks(query)

        if not tracks:
            return await ctx.send('Nothing found!')

        embed = discord.Embed(color=discord.Color.blurple())

        if 'list' in query and 'ytsearch:' not in query:
            for track in tracks:
                player.add(requester=ctx.author.id, track=track)

            embed.title = 'Playlist enqueued!'
            embed.description = f'Imported {len(tracks)} tracks from the playlist!'
            await ctx.send(embed=embed)
        else:
            track_title = tracks[0]["info"]["title"]
            track_uri = tracks[0]["info"]["uri"]

            embed.title = "Track enqueued!"
            embed.description = f'[{track_title}]({track_uri})'
            player.add(requester=ctx.author.id, track=tracks[0])

        if not player.is_playing:
            await player.play()