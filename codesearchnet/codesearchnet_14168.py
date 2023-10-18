def live_source_load(self, source):
        """
        Send new source code to the bot

        :param source:
        :param good_cb: callback called if code was good
        :param bad_cb: callback called if code was bad (will get contents of exception)
        :return:
        """
        source = source.rstrip('\n')
        if source != self.source:
            self.source = source
            b64_source = base64.b64encode(bytes(bytearray(source, "ascii")))
            self.send_command(CMD_LOAD_BASE64, b64_source)