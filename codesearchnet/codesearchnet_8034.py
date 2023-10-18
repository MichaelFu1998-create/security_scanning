def create_index(self, fields, no_term_offsets=False,
                     no_field_flags=False, stopwords = None):
        """
        Create the search index. The index must not already exist.

        ### Parameters:

        - **fields**: a list of TextField or NumericField objects
        - **no_term_offsets**: If true, we will not save term offsets in the index
        - **no_field_flags**: If true, we will not save field flags that allow searching in specific fields
        - **stopwords**: If not None, we create the index with this custom stopword list. The list can be empty
        """

        args = [self.CREATE_CMD, self.index_name]
        if no_term_offsets:
            args.append(self.NOOFFSETS)
        if no_field_flags:
            args.append(self.NOFIELDS)
        if stopwords is not None and isinstance(stopwords, (list, tuple, set)):
            args += [self.STOPWORDS, len(stopwords)]
            if len(stopwords) > 0:
                args += list(stopwords)
    
        args.append('SCHEMA')

        args += list(itertools.chain(*(f.redis_args() for f in fields)))

        return self.redis.execute_command(*args)