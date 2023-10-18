def _update_handlers(self):
        """Update `_handler_map` after `handlers` have been
        modified."""
        handler_map = defaultdict(list)
        for i, obj in enumerate(self.handlers):
            for dummy, handler in inspect.getmembers(obj, callable):
                if not hasattr(handler, "_pyxmpp_event_handled"):
                    continue
                # pylint: disable-msg=W0212
                event_class = handler._pyxmpp_event_handled
                handler_map[event_class].append( (i, handler) )
        self._handler_map = handler_map