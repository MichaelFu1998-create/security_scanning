def table_row(self, content):
        """Rendering a table row. Like ``<tr>``.

        :param content: content of current table row.
        """
        contents = content.splitlines()
        if not contents:
            return ''
        clist = ['* ' + contents[0]]
        if len(contents) > 1:
            for c in contents[1:]:
                clist.append('  ' + c)
        return '\n'.join(clist) + '\n'