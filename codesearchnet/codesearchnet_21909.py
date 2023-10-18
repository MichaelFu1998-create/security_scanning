def get_lines_data(self):
        """
        Returns string:line_numbers list
        Since all strings are unique it is OK to get line numbers this way.
        Since same string can occur several times inside single .json file the values should be popped(FIFO) from the list
        :rtype: list
        """

        encoding = 'utf-8'

        for token in tokenize(self.data.decode(encoding)):
            if token.type == 'operator':
                if token.value == '{':
                    self.start_object()
                elif token.value ==':':
                    self.with_separator(token)
                elif token.value == '}':
                    self.end_object()
                elif token.value == ',':
                    self.end_pair()


            elif token.type=='string':
                if self.state=='key':
                    self.current_key=unquote_string(token.value)
                    if self.current_key==JSON_GETTEXT_KEYWORD:
                        self.gettext_mode=True

                #==value not actually used, but if only key was met (like in list) it still will be used. The important part, that key wont be parsed as value, not reversal
                if self.gettext_mode:
                    if self.current_key==JSON_GETTEXT_KEY_CONTENT:
                        self.token_to_add=token
                    elif self.current_key==JSON_GETTEXT_KEY_ALT_CONTENT:
                        self.token_params['alt_token']=token
                    elif self.current_key==JSON_GETTEXT_KEY_FUNCNAME:
                        self.token_params['funcname']=token.value
                else:
                    self.token_to_add=token

        return self.results