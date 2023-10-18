def info(self):
        """
        Get info an stats about the the current index, including the number of documents, memory consumption, etc
        """

        res = self.redis.execute_command('FT.INFO', self.index_name)
        it = six.moves.map(to_string, res)
        return dict(six.moves.zip(it, it))