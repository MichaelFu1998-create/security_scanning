def summarize(self, fields=None, context_len=None, num_frags=None, sep=None):
        """
        Return an abridged format of the field, containing only the segments of
        the field which contain the matching term(s).

        If `fields` is specified, then only the mentioned fields are
        summarized; otherwise all results are summarized.

        Server side defaults are used for each option (except `fields`) if not specified

        - **fields** List of fields to summarize. All fields are summarized if not specified
        - **context_len** Amount of context to include with each fragment
        - **num_frags** Number of fragments per document
        - **sep** Separator string to separate fragments
        """
        args = ['SUMMARIZE']
        fields = self._mk_field_list(fields)
        if fields:
            args += ['FIELDS', str(len(fields))] + fields

        if context_len is not None:
            args += ['LEN', str(context_len)]
        if num_frags is not None:
            args += ['FRAGS', str(num_frags)]
        if sep is not None:
            args += ['SEPARATOR', sep]

        self._summarize_fields = args
        return self