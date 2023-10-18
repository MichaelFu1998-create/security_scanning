def __try_handlers(self, handler_list, stanza, stanza_type = None):
        """ Search the handler list for handlers matching
        given stanza type and payload namespace. Run the
        handlers found ordering them by priority until
        the first one which returns `True`.

        :Parameters:
            - `handler_list`: list of available handlers
            - `stanza`: the stanza to handle
            - `stanza_type`: stanza type override (value of its "type"
              attribute)

        :return: result of the last handler or `False` if no
            handler was found.
        """
        # pylint: disable=W0212
        if stanza_type is None:
            stanza_type = stanza.stanza_type
        payload = stanza.get_all_payload()
        classes = [p.__class__ for p in payload]
        keys = [(p.__class__, p.handler_key) for p in payload]
        for handler in handler_list:
            type_filter = handler._pyxmpp_stanza_handled[1]
            class_filter = handler._pyxmpp_payload_class_handled
            extra_filter = handler._pyxmpp_payload_key
            if type_filter != stanza_type:
                continue
            if class_filter:
                if extra_filter is None and class_filter not in classes:
                    continue
                if extra_filter and (class_filter, extra_filter) not in keys:
                    continue
            response = handler(stanza)
            if self._process_handler_result(response):
                return True
        return False