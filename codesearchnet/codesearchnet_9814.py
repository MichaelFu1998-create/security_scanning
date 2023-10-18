def create_table(self, conn):
        """Make table definitions"""
        # Make cursor
        cur = conn.cursor()
        # Drop table if it already exists, to be recreated.  This
        # could in the future abort if table already exists, and not
        # recreate it from scratch.
        #cur.execute('''DROP TABLE IF EXISTS %s'''%self.table)
        #conn.commit()
        if self.tabledef is None:
            return
        if not self.tabledef.startswith('CREATE'):
            # "normal" table creation.
            cur.execute('CREATE TABLE IF NOT EXISTS %s %s'
                        % (self.table, self.tabledef)
                        )
        else:
            # When tabledef contains the full CREATE statement (for
            # virtual tables).
            cur.execute(self.tabledef)
        conn.commit()