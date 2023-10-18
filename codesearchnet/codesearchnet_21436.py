def shrink_indexes_in_place(self, triples):
        """Uses a union find to find segment."""

        _ent_roots = self.UnionFind(self._ent_id)
        _rel_roots = self.UnionFind(self._rel_id)

        for t in triples:
            _ent_roots.add(t.head)
            _ent_roots.add(t.tail)
            _rel_roots.add(t.relation)

        for i, t in enumerate(triples):
            h = _ent_roots.find(t.head)
            r = _rel_roots.find(t.relation)
            t = _ent_roots.find(t.tail)
            triples[i] = kgedata.TripleIndex(h, r, t)

        ents = bidict()
        available_ent_idx = 0
        for previous_idx, ent_exist in enumerate(_ent_roots.roots()):
            if not ent_exist:
                self._ents.inverse.pop(previous_idx)
            else:
                ents[self._ents.inverse[previous_idx]] = available_ent_idx
            available_ent_idx += 1
        rels = bidict()
        available_rel_idx = 0
        for previous_idx, rel_exist in enumerate(_rel_roots.roots()):
            if not rel_exist:
                self._rels.inverse.pop(previous_idx)
            else:
                rels[self._rels.inverse[previous_idx]] = available_rel_idx
            available_rel_idx += 1
        self._ents = ents
        self._rels = rels
        self._ent_id = available_ent_idx
        self._rel_id = available_rel_idx