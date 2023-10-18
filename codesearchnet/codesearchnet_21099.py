def intersection(self, other, recursive=True):
        """
        Recursively compute intersection of data. For dictionaries, items
        for specific keys will be reduced to unique items. For lists, items
        will be reduced to unique items. This method is meant to be analogous
        to set.intersection for composite objects.

        Args:
            other (composite): Other composite object to intersect with.
            recursive (bool): Whether or not to perform the operation recursively,
                for all nested composite objects.
        """
        if not isinstance(other, composite):
            raise AssertionError('Cannot intersect composite and {} types'.format(type(other)))
        
        if self.meta_type != other.meta_type:
            return composite({})

        if self.meta_type == 'list':
            keep = []
            for item in self._list:
                if item in other._list:
                    if recursive and isinstance(item, composite):
                        keep.extend(item.intersection(other.index(item), recursive=True))
                    else:
                        keep.append(item)
            return composite(keep)
        elif self.meta_type == 'dict':
            keep = {}
            for key in self._dict:
                item = self._dict[key]
                if key in other._dict:
                    if recursive and \
                       isinstance(item, composite) and \
                       isinstance(other.get(key), composite):
                       keep[key] = item.intersection(other.get(key), recursive=True)
                    elif item == other[key]:
                        keep[key] = item
            return composite(keep)
        return