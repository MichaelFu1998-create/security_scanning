def is_subset_of(self, *supersets):
        """Asserts that val is iterable and a subset of the given superset or flattened superset if multiple supersets are given."""
        if not isinstance(self.val, Iterable):
            raise TypeError('val is not iterable')
        if len(supersets) == 0:
            raise ValueError('one or more superset args must be given')

        missing = []
        if hasattr(self.val, 'keys') and callable(getattr(self.val, 'keys')) and hasattr(self.val, '__getitem__'):
            # flatten superset dicts
            superdict = {}
            for l,j in enumerate(supersets):
                self._check_dict_like(j, check_values=False, name='arg #%d' % (l+1))
                for k in j.keys():
                    superdict.update({k: j[k]})

            for i in self.val.keys():
                if i not in superdict:
                    missing.append({i: self.val[i]}) # bad key
                elif self.val[i] != superdict[i]:
                    missing.append({i: self.val[i]}) # bad val
            if missing:
                self._err('Expected <%s> to be subset of %s, but %s %s missing.' % (self.val, self._fmt_items(superdict), self._fmt_items(missing), 'was' if len(missing) == 1 else 'were'))
        else:
            # flatten supersets
            superset = set()
            for j in supersets:
                try:
                    for k in j:
                        superset.add(k)
                except Exception:
                    superset.add(j)

            for i in self.val:
                if i not in superset:
                    missing.append(i)
            if missing:
                self._err('Expected <%s> to be subset of %s, but %s %s missing.' % (self.val, self._fmt_items(superset), self._fmt_items(missing), 'was' if len(missing) == 1 else 'were'))

        return self