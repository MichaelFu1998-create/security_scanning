def settings(self):
        """Returns settings from the server."""
        stmt = "select {fields} from pg_settings".format(fields=', '.join(SETTINGS_FIELDS))
        settings = []
        for row in self._iter_results(stmt):
            row['setting'] = self._vartype_map[row['vartype']](row['setting'])
            settings.append(Settings(**row))
        return settings