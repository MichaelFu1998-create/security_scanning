def db_value(self, value):
        """Convert the python value for storage in the database."""
        value = self.transform_value(value)
        return self.hhash.encrypt(value, 
            salt_size=self.salt_size, rounds=self.rounds)