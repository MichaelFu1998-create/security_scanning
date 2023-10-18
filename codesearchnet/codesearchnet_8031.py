def add_suggestions(self,  *suggestions, **kwargs):
        """
        Add suggestion terms to the AutoCompleter engine. Each suggestion has a score and string.

        If kwargs['increment'] is true and the terms are already in the server's dictionary, we increment their scores
        """
        pipe = self.redis.pipeline()
        for sug in suggestions:
            args = [AutoCompleter.SUGADD_COMMAND, self.key, sug.string, sug.score]
            if kwargs.get('increment'):
                args.append(AutoCompleter.INCR)
            if sug.payload:
                args.append('PAYLOAD')
                args.append(sug.payload)

            pipe.execute_command(*args)

        return pipe.execute()[-1]