def write(self, _force=False, _exists_ok=False, **items):
        """
        Creates a db file with the core schema.

        :param force: If `True` an existing db file will be overwritten.
        """
        if self.fname and self.fname.exists():
            raise ValueError('db file already exists, use force=True to overwrite')

        with self.connection() as db:
            for table in self.tables:
                db.execute(table.sql(translate=self.translate))

            db.execute('PRAGMA foreign_keys = ON;')
            db.commit()

            refs = defaultdict(list)  # collects rows in association tables.
            for t in self.tables:
                if t.name not in items:
                    continue
                rows, keys = [], []
                cols = {c.name: c for c in t.columns}
                for i, row in enumerate(items[t.name]):
                    pk = row[t.primary_key[0]] \
                        if t.primary_key and len(t.primary_key) == 1 else None
                    values = []
                    for k, v in row.items():
                        if k in t.many_to_many:
                            assert pk
                            at = t.many_to_many[k]
                            atkey = tuple([at.name] + [c.name for c in at.columns])
                            for vv in v:
                                fkey, context = self.association_table_context(t, k, vv)
                                refs[atkey].append((pk, fkey, context))
                        else:
                            col = cols[k]
                            if isinstance(v, list):
                                # Note: This assumes list-valued columns are of datatype string!
                                v = (col.separator or ';').join(
                                    col.convert(vv) for vv in v)
                            else:
                                v = col.convert(v) if v is not None else None
                            if i == 0:
                                keys.append(col.name)
                            values.append(v)
                    rows.append(tuple(values))
                insert(db, self.translate, t.name, keys, *rows)

            for atkey, rows in refs.items():
                insert(db, self.translate, atkey[0], atkey[1:], *rows)

            db.commit()