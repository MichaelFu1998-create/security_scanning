def _validate_no_null_values(self):
        """
        Loads the tables from the gtfs object and counts the number of rows that have null values in
        fields that should not be null. Stores the number of null rows in warnings_container
        """
        for table in DB_TABLE_NAMES:
            null_not_ok_warning = "Null values in must-have columns in table {table}".format(table=table)
            null_warn_warning = "Null values in good-to-have columns in table {table}".format(table=table)
            null_not_ok_fields = DB_TABLE_NAME_TO_FIELDS_WHERE_NULL_NOT_OK[table]
            null_warn_fields = DB_TABLE_NAME_TO_FIELDS_WHERE_NULL_OK_BUT_WARN[table]

            # CW, TODO: make this validation source by source
            df = self.gtfs.get_table(table)

            for warning, fields in zip([null_not_ok_warning, null_warn_warning], [null_not_ok_fields, null_warn_fields]):
                null_unwanted_df = df[fields]
                rows_having_null = null_unwanted_df.isnull().any(1)
                if sum(rows_having_null) > 0:
                    rows_having_unwanted_null = df[rows_having_null.values]
                    self.warnings_container.add_warning(warning, rows_having_unwanted_null, len(rows_having_unwanted_null))