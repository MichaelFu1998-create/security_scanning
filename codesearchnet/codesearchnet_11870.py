def load_db_set(self, name, r=None):
        """
        Loads database parameters from a specific named set.
        """
        r = r or self
        db_set = r.genv.db_sets.get(name, {})
        r.genv.update(db_set)