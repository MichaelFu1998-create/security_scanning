def set(self, key, value):
        """ Set key value """
        if self.in_memory:
            self._memory_db[key] = value
        else:
            db = self._read_file()
            db[key] = value
            with open(self.db_path, 'w') as f:
                f.write(json.dumps(db, ensure_ascii=False, indent=2))