def format_answers(self, fmt='obj'):
        """Formats answers depending on `fmt`.
        """
        fmts = ('obj', 'array', 'plain')
        if fmt not in fmts:
            eprint("Error: '{}' not in {}".format(fmt, fmts))
            return

        def stringify(val):
            if type(val) in (list, tuple):
                return ', '.join(str(e) for e in val)
            return val

        if fmt == 'obj':
            return json.dumps(self.answers)
        elif fmt == 'array':
            answers = [[k, v] for k, v in self.answers.items()]
            return json.dumps(answers)
        elif fmt == 'plain':
            answers = '\n'.join('{}: {}'.format(k, stringify(v)) for k, v in self.answers.items())
            return answers