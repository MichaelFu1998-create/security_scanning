def setup_stanza_handlers(self, handler_objects, usage_restriction):
        """Install stanza handlers provided by `handler_objects`"""
        # pylint: disable=W0212
        iq_handlers = {"get": {}, "set": {}}
        message_handlers = []
        presence_handlers = []
        for obj in handler_objects:
            if not isinstance(obj, XMPPFeatureHandler):
                continue
            obj.stanza_processor = self
            for dummy, handler in inspect.getmembers(obj, callable):
                if not hasattr(handler, "_pyxmpp_stanza_handled"):
                    continue
                element_name, stanza_type = handler._pyxmpp_stanza_handled
                restr = handler._pyxmpp_usage_restriction
                if restr and restr != usage_restriction:
                    continue
                if element_name == "iq":
                    payload_class = handler._pyxmpp_payload_class_handled
                    payload_key = handler._pyxmpp_payload_key
                    if (payload_class, payload_key) in iq_handlers[stanza_type]:
                        continue
                    iq_handlers[stanza_type][(payload_class, payload_key)] = \
                            handler
                    continue
                elif element_name == "message":
                    handler_list = message_handlers
                elif element_name == "presence":
                    handler_list = presence_handlers
                else:
                    raise ValueError, "Bad handler decoration"
                handler_list.append(handler)
        with self.lock:
            self._iq_handlers = iq_handlers
            self._presence_handlers = presence_handlers
            self._message_handlers = message_handlers