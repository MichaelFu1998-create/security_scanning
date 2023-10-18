def table(self, header, body):
        """Rendering table element. Wrap header and body in it.

        :param header: header part of the table.
        :param body: body part of the table.
        """
        table = '\n.. list-table::\n'
        if header and not header.isspace():
            table = (table + self.indent + ':header-rows: 1\n\n' +
                     self._indent_block(header) + '\n')
        else:
            table = table + '\n'
        table = table + self._indent_block(body) + '\n\n'
        return table