def delete(self, string):
        """
        Delete a string from the AutoCompleter index.
        Returns 1 if the string was found and deleted, 0 otherwise
        """
        return self.redis.execute_command(AutoCompleter.SUGDEL_COMMAND, self.key, string)