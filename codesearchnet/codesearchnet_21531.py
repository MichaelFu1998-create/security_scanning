def connections(self, name):
        """Returns a list of existing connections to the named database."""
        stmt = """
            select {fields} from pg_stat_activity
            where datname = {datname!r} and pid <> pg_backend_pid()
        """.format(fields=', '.join(CONNECTION_FIELDS), datname=name)
        return list(Connection(**x) for x in self._iter_results(stmt))