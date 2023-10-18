def _setup_stream_element_handlers(self):
        """Set up stream element handlers.

        Scans the `handlers` list for `StreamFeatureHandler`
        instances and updates `_element_handlers` mapping with their
        methods decorated with @`stream_element_handler`
        """
        # pylint: disable-msg=W0212
        if self.initiator:
            mode = "initiator"
        else:
            mode = "receiver"
        self._element_handlers = {}
        for handler in self.handlers:
            if not isinstance(handler, StreamFeatureHandler):
                continue
            for _unused, meth in inspect.getmembers(handler, callable):
                if not hasattr(meth, "_pyxmpp_stream_element_handled"):
                    continue
                element_handled = meth._pyxmpp_stream_element_handled
                if element_handled in self._element_handlers:
                    # use only the first matching handler
                    continue
                if meth._pyxmpp_usage_restriction in (None, mode):
                    self._element_handlers[element_handled] = meth