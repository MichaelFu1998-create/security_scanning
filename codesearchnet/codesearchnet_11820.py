def load_table(self, table_name, src, dst='localhost', name=None, site=None):
        """
        Directly transfers a table between two databases.
        """
        #TODO: incomplete
        r = self.database_renderer(name=name, site=site)
        r.env.table_name = table_name
        r.run('psql --user={dst_db_user} --host={dst_db_host} --command="DROP TABLE IF EXISTS {table_name} CASCADE;"')
        r.run('pg_dump -t {table_name} --user={dst_db_user} --host={dst_db_host} | psql --user={src_db_user} --host={src_db_host}')