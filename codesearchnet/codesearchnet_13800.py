def do_prompt(self, arg):
        """
        Enable or disable prompt
        :param arg: on|off
        :return:
        """
        if arg.lower() == 'off':
            self.response_prompt = ''
            self.prompt = ''
            return
        elif arg.lower() == 'on':
            self.prompt = PROMPT
            self.response_prompt = RESPONSE_PROMPT
        self.print_response('prompt: %s' % self.prompt, '\n', 'response: %s' % self.response_prompt)