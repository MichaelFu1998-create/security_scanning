def _bulk_insert_into_app_models(self, cursor, app_model, fields, db_values, placeholder_list):
        """
        Example query:
        `REPLACE INTO model (F1,F2,F3) VALUES (%s, %s, %s), (%s, %s, %s), (%s, %s, %s)`
        where values=[1,2,3,4,5,6,7,8,9]
        """
        # calculate and create equal sized chunks of data to insert incrementally
        num_of_rows_able_to_insert = self.SQLITE_MAX_VARIABLE_NUMBER // len(fields)
        num_of_values_able_to_insert = num_of_rows_able_to_insert * len(fields)
        value_chunks = [db_values[x:x + num_of_values_able_to_insert] for x in range(0, len(db_values), num_of_values_able_to_insert)]
        placeholder_chunks = [placeholder_list[x: x + num_of_rows_able_to_insert] for x in range(0, len(placeholder_list), num_of_rows_able_to_insert)]
        # insert data chunks
        fields = str(tuple(str(f.attname) for f in fields)).replace("'", '')
        for values, params in zip(value_chunks, placeholder_chunks):
            placeholder_str = ', '.join(params).replace("'", '')
            insert = """REPLACE INTO {app_model} {fields}
                        VALUES {placeholder_str}
            """.format(app_model=app_model, fields=fields, placeholder_str=placeholder_str)
            # use DB-APIs parameter substitution (2nd parameter expects a sequence)
            cursor.execute(insert, values)