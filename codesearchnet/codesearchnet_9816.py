def import_(self, conn):
        """Do the actual import. Copy data and store in connection object.

        This function:
        - Creates the tables
        - Imports data (using self.gen_rows)
        - Run any post_import hooks.
        - Creates any indexs
        - Does *not* run self.make_views - those must be done
          after all tables are loaded.
        """
        if self.print_progress:
            print('Beginning', self.__class__.__name__)
        # what is this mystical self._conn ?
        self._conn = conn

        self.create_table(conn)
        # This does insertions
        if self.mode in ('all', 'import') and self.fname and self.exists() and self.table not in ignore_tables:
            self.insert_data(conn)
        # This makes indexes in the DB.
        if self.mode in ('all', 'index') and hasattr(self, 'index'):
            self.create_index(conn)
        # Any post-processing to be done after the full import.
        if self.mode in ('all', 'import') and hasattr(self, 'post_import'):
            self.run_post_import(conn)
        # Commit it all
        conn.commit()