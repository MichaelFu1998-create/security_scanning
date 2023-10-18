def delete(self, key_name):
        """Delete the key and return true if the key was deleted, else false
        """
        self.db.remove(Query().name == key_name)
        return self.get(key_name) == {}