def _sort(self, concepts, sort=None, language='any', reverse=False):
        '''
        Returns a sorted version of a list of concepts. Will leave the original
        list unsorted.

        :param list concepts: A list of concepts and collections.
        :param string sort: What to sort on: `id`, `label` or `sortlabel`
        :param string language: Language to use when sorting on `label` or
            `sortlabel`.
        :param boolean reverse: Reverse the sort order?
        :rtype: list
        '''
        sorted = copy.copy(concepts)
        if sort:
            sorted.sort(key=methodcaller('_sortkey', sort, language), reverse=reverse)
        return sorted