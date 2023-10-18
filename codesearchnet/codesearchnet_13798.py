def print_response(self, input='', keep=False, *args, **kwargs):
        """
        print response, if cookie is set then print that each line
        :param args:
        :param keep: if True more output is to come
        :param cookie: set a custom cookie,
                       if set to 'None' then self.cookie will be used.
                       if set to 'False' disables cookie output entirely
        :return:
        """
        cookie = kwargs.get('cookie')
        if cookie is None:
            cookie = self.cookie or ''
        status = kwargs.get('status')
        lines = input.splitlines()
        if status and not lines:
            lines = ['']

        if cookie:
            output_template = '{cookie} {status}{cookie_char}{line}'
        else:
            output_template = '{line}'

        for i, line in enumerate(lines):
            if i != len(lines) - 1 or keep is True:
                cookie_char = '>'
            else:
                # last line
                cookie_char = ':'

            print(output_template.format(
                cookie_char=cookie_char,
                cookie=cookie,
                status=status or '',
                line=line.strip()), file=self.stdout)