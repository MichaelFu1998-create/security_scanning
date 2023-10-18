def do_load_base64(self, line):
        """
        load filename=(file)
        load base64=(base64 encoded)

        Send new code to shoebot.

        If it does not run successfully shoebot will attempt to role back.

        Editors can enable livecoding by sending new code as it is edited.
        """
        cookie = self.cookie
        executor = self.bot._executor

        def source_good():
            self.print_response(status=RESPONSE_CODE_OK, cookie=cookie)
            executor.clear_callbacks()

        def source_bad(tb):
            if called_good:
                # good and bad callbacks shouldn't both be called
                raise ValueError('Good AND Bad callbacks called !')
            self.print_response(status=RESPONSE_REVERTED, keep=True, cookie=cookie)
            self.print_response(tb.replace('\n', '\\n'), cookie=cookie)
            executor.clear_callbacks()

        called_good = False
        source = str(base64.b64decode(line))
        # Test compile
        publish_event(SOURCE_CHANGED_EVENT, data=source, extra_channels="shoebot.source")
        self.bot._executor.load_edited_source(source, good_cb=source_good, bad_cb=source_bad)