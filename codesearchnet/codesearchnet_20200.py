def get_schema(self, filename):
        """
        Guess schema using messytables
        """
        table_set = self.read_file(filename)
            
        # Have I been able to read the filename
        if table_set is None: 
            return [] 

        # Get the first table as rowset
        row_set = table_set.tables[0]

        offset, headers = headers_guess(row_set.sample)
        row_set.register_processor(headers_processor(headers))
        row_set.register_processor(offset_processor(offset + 1))
        types = type_guess(row_set.sample, strict=True)

        # Get a sample as well..
        sample = next(row_set.sample)

        clean = lambda v: str(v) if not isinstance(v, str) else v 
        schema = []
        for i, h in enumerate(headers):
            schema.append([h,
                           str(types[i]),
                           clean(sample[i].value)])

        return schema