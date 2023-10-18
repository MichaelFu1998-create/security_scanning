def get_args(self):
        """
        Format the redis arguments for this query and return them
        """

        args = [self._query_string]

        if self._no_content:
            args.append('NOCONTENT')

        if self._fields:

            args.append('INFIELDS')
            args.append(len(self._fields))
            args += self._fields
        
        if self._verbatim:
            args.append('VERBATIM')

        if self._no_stopwords:
            args.append('NOSTOPWORDS')

        if self._filters:
            for flt in self._filters:
                assert isinstance(flt, Filter)
                args += flt.args

        if self._with_payloads:
            args.append('WITHPAYLOADS')
        
        if self._ids:
            args.append('INKEYS')
            args.append(len(self._ids))
            args += self._ids

        if self._slop >= 0:
            args += ['SLOP', self._slop]

        if self._in_order:
            args.append('INORDER')

        if self._return_fields:
            args.append('RETURN')
            args.append(len(self._return_fields))
            args += self._return_fields

        if self._sortby:
            assert isinstance(self._sortby, SortbyField)
            args.append('SORTBY')
            args += self._sortby.args

        if self._language:
            args += ['LANGUAGE', self._language]

        args += self._summarize_fields + self._highlight_fields
        args += ["LIMIT", self._offset, self._num]
        return args