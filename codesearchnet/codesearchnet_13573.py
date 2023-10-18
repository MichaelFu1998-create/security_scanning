def set_handlers(self,priority=10):
        """
        Assign MUC stanza handlers to the `self.stream`.

        :Parameters:
            - `priority`: priority for the handlers.
        :Types:
            - `priority`: `int`
        """
        self.stream.set_message_handler("groupchat",self.__groupchat_message,None,priority)
        self.stream.set_message_handler("error",self.__error_message,None,priority)
        self.stream.set_presence_handler("available",self.__presence_available,None,priority)
        self.stream.set_presence_handler("unavailable",self.__presence_unavailable,None,priority)
        self.stream.set_presence_handler("error",self.__presence_error,None,priority)