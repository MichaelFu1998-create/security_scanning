async def _load(self):
        """Load more events for this conversation."""
        try:
            conv_events = await self._conversation.get_events(
                self._conversation.events[0].id_
            )
        except (IndexError, hangups.NetworkError):
            conv_events = []
        if not conv_events:
            self._first_loaded = True
        if self._focus_position == self.POSITION_LOADING and conv_events:
            # If the loading indicator is still focused, and we loaded more
            # events, set focus on the first new event so the loaded
            # indicator is replaced.
            self.set_focus(conv_events[-1].id_)
        else:
            # Otherwise, still need to invalidate in case the loading
            # indicator is showing but not focused.
            self._modified()
        # Loading events can also update the watermarks.
        self._refresh_watermarked_events()
        self._is_loading = False