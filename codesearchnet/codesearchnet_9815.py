def insert_data(self, conn):
        """Load data from GTFS file into database"""
        cur = conn.cursor()
        # This is a bit hackish.  It is annoying to have to write the
        # INSERT statement yourself and keep it up to date with the
        # table rows.  This gets the first row, figures out the field
        # names from that, and then makes an INSERT statement like
        # "INSERT INTO table (col1, col2, ...) VALUES (:col1, :col2,
        # ...)".  The ":col1" is sqlite syntax for named value.

        csv_reader_generators, prefixes = self._get_csv_reader_generators()
        for csv_reader, prefix in zip(csv_reader_generators, prefixes):
            try:
                row = next(iter(self.gen_rows([csv_reader], [prefix])))
                fields = row.keys()
            except StopIteration:
                # The file has *only* a header and no data.
                # next(iter()) yields StopIteration and we can't
                # proceed.  Since there is nothing to import, just continue the loop
                print("Not importing %s into %s for %s" % (self.fname, self.table, prefix))
                continue
            stmt = '''INSERT INTO %s (%s) VALUES (%s)''' % (
                self.table,
                (', '.join([x for x in fields if x[0] != '_'] + self.extra_keys)),
                (', '.join([":" + x for x in fields if x[0] != '_'] + self.extra_values))
            )

            # This does the actual insertions.  Passed the INSERT
            # statement and then an iterator over dictionaries.  Each
            # dictionary is inserted.
            if self.print_progress:
                print('Importing %s into %s for %s' % (self.fname, self.table, prefix))
            # the first row was consumed by fetching the fields
            # (this could be optimized)
            from itertools import chain
            rows = chain([row], self.gen_rows([csv_reader], [prefix]))
            cur.executemany(stmt, rows)
            conn.commit()