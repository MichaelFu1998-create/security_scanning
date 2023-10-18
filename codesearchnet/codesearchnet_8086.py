def _iter_children(self, url, kind, klass, recurse=None):
        """Iterate over all children of `kind`

        Yield an instance of `klass` when a child is of type `kind`. Uses
        `recurse` as the path of attributes in the JSON returned from `url`
        to find more children.
        """
        children = self._follow_next(url)

        while children:
            child = children.pop()
            kind_ = child['attributes']['kind']
            if kind_ == kind:
                yield klass(child, self.session)
            elif recurse is not None:
                # recurse into a child and add entries to `children`
                url = self._get_attribute(child, *recurse)
                children.extend(self._follow_next(url))