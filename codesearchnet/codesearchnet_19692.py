def _parse_dumb_push_output(self, string):
        """since the push process outputs a single unicode string consisting of
        multiple JSON formatted "status" lines, we need to parse it so that it
        can be read as multiple strings.

        This will receive the string as an input, count curly braces and ignore
        any newlines. When the curly braces stack is 0, it will append the
        entire string it has read up until then to a list and so forth.

        :param string: the string to parse
        :rtype: list of JSON's
        """
        stack = 0
        json_list = []
        tmp_json = ''
        for char in string:
            if not char == '\r' and not char == '\n':
                tmp_json += char
            if char == '{':
                stack += 1
            elif char == '}':
                stack -= 1
            if stack == 0:
                if not len(tmp_json) == 0:
                    json_list.append(tmp_json)
                tmp_json = ''
        return json_list