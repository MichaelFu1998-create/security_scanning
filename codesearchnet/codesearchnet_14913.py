def complete(code, line, column, path, encoding, prefix):
        """
        Completes python code using `jedi`_.

        :returns: a list of completion.
        """
        ret_val = []
        try:
            script = jedi.Script(code, line + 1, column, path, encoding)
            completions = script.completions()
            print('completions: %r' % completions)
        except jedi.NotFoundError:
            completions = []
        for completion in completions:
            ret_val.append({
                'name': completion.name,
                'icon': icon_from_typename(
                    completion.name, completion.type),
                'tooltip': completion.description})
        return ret_val