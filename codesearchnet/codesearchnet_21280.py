def insert_dict(self, value_dict, commit=False):
        """ 
        Execute an INSERT statement using a python dict

        :value_dict:    A dictionary representing all the columns(keys) and 
            values that should be part of the INSERT statement
        :commit:        Whether to automatically commit the transaction
        :returns:       Psycopg2 result
        """

        # Sanity check the value_dict
        for key in value_dict.keys():
            if key not in self.columns:
                raise ValueError("Column %s does not exist" % key)

        # These lists will make up the columns and values of the INSERT
        insert_cols = []
        value_set = []

        # Go through all the possible columns and look for that column in the
        # dict.  If available, we need to add it to our col/val sets
        for col in self.columns:
            if col in value_dict:
                #log.debug("Inserting with column %s" % col)
                insert_cols.append(col)
                value_set.append(value_dict[col])

        # Create SQL statement placeholders for the dynamic values
        placeholders = ', '.join(["{%s}" % x for x in range(1, len(value_set) + 1)])

        # TODO: Maybe don't trust table_name ane pk_name?  Shouldn't really be 
        # user input, but who knows.
        query = self._assemble_with_columns('''
            INSERT INTO "''' + self.table + '''" ({0}) 
            VALUES (''' + placeholders + ''') 
            RETURNING ''' + self.pk + '''
            ''', insert_cols, *value_set)

        result = self._execute(query, commit=commit)

        # Inca
        if len(result) > 0:
            # Return the pk if we can
            if hasattr(result[0], self.pk):
                return getattr(result[0], self.pk)
            # Otherwise, the full result
            else:
                return result[0]
        else:
            return None