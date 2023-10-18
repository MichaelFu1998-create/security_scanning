def add_soft_foreign_key(cls, column, table_name, alias=None):
        """
        the column stores foreign table's primary key but isn't a foreign key (to avoid constraint)
        warning: if the table not exists, will crash when query with loadfk
        :param column: table's column
        :param table_name: foreign table name
        :param alias: table name's alias. Default is as same as table name.
        :return: True, None
        """
        if column in cls.fields:
            table = SQLForeignKey(table_name, column, cls.fields[column], True)

            if alias:
                if alias in cls.foreign_keys_table_alias:
                    logger.warning("This alias of table is already exists, overwriting: %s.%s to %s" %
                                   (cls.__name__, column, table_name))
                cls.foreign_keys_table_alias[alias] = table

            if column not in cls.foreign_keys:
                cls.foreign_keys[column] = [table]
            else:
                if not alias:
                    logger.warning("The soft foreign key will not work, an alias required: %s.%s to %r" %
                                   (cls.__name__, column, table_name))
                cls.foreign_keys[column].append(table)
            return True