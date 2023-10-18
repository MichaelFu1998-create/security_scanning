def _sortkey(self, key='uri', language='any'):
        '''
        Provide a single sortkey for this conceptscheme.

        :param string key: Either `uri`, `label` or `sortlabel`.
        :param string language: The preferred language to receive the label in
            if key is `label` or `sortlabel`. This should be a valid IANA language tag.
        :rtype: :class:`str`
        '''
        if key == 'uri':
            return self.uri
        else:
            l = label(self.labels, language, key == 'sortlabel')
            return l.label.lower() if l else ''