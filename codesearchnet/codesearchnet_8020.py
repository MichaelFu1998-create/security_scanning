async def dispatch_event(self, event):
        """ Dispatches an event to all registered hooks. """
        log.debug('Dispatching event of type {} to {} hooks'.format(event.__class__.__name__, len(self.hooks)))
        for hook in self.hooks:
            try:
                if asyncio.iscoroutinefunction(hook):
                    await hook(event)
                else:
                    hook(event)
            except Exception as e:  # pylint: disable=broad-except
                # Catch generic exception thrown by user hooks
                log.warning(
                    'Encountered exception while dispatching an event to hook `{}` ({})'.format(hook.__name__, str(e)))

        if isinstance(event, (TrackEndEvent, TrackExceptionEvent, TrackStuckEvent)) and event.player:
            await event.player.handle_event(event)