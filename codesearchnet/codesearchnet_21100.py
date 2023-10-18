def union(self, other, recursive=True, overwrite=False):
        """
        Recursively compute union of data. For dictionaries, items
        for specific keys will be combined into a list, depending on the
        status of the overwrite= parameter. For lists, items will be appended
        and reduced to unique items. This method is meant to be analogous
        to set.union for composite objects.

        Args:
            other (composite): Other composite object to union with.
            recursive (bool): Whether or not to perform the operation recursively,
                for all nested composite objects.
            overwrite (bool): Whether or not to overwrite entries with the same
                key in a nested dictionary. 
        """
        if not isinstance(other, composite):
            raise AssertionError('Cannot union composite and {} types'.format(type(other)))
        
        if self.meta_type != other.meta_type:
            return composite([self, other])

        if self.meta_type == 'list':
            keep = []
            for item in self._list:
                keep.append(item)
            for item in other._list:
                if item not in self._list:
                    keep.append(item)
            return composite(keep)
        elif self.meta_type == 'dict':
            keep = {}
            for key in list(set(list(self._dict.keys()) + list(other._dict.keys()))):
                left = self._dict.get(key)
                right = other._dict.get(key)
                if recursive and \
                   isinstance(left, composite) and \
                   isinstance(right, composite):
                    keep[key] = left.union(right, recursive=recursive, overwrite=overwrite)
                elif left == right:
                    keep[key] = left
                elif left is None:
                    keep[key] = right
                elif right is None:
                    keep[key] = left
                elif overwrite:
                    keep[key] = right
                else:
                    keep[key] = composite([left, right])
            return composite(keep)
        return