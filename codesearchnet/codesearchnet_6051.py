def get_content(self):
        """Open content as a stream for reading.

        See DAVResource.get_content()
        """
        filestream = compat.StringIO()

        tableName, primKey = self.provider._split_path(self.path)
        if primKey is not None:
            conn = self.provider._init_connection()
            listFields = self.provider._get_field_list(conn, tableName)
            csvwriter = csv.DictWriter(filestream, listFields, extrasaction="ignore")
            dictFields = {}
            for field_name in listFields:
                dictFields[field_name] = field_name
            csvwriter.writerow(dictFields)

            if primKey == "_ENTIRE_CONTENTS":
                cursor = conn.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT * from " + self.provider._db + "." + tableName)
                result_set = cursor.fetchall()
                for row in result_set:
                    csvwriter.writerow(row)
                cursor.close()
            else:
                row = self.provider._get_record_by_primary_key(conn, tableName, primKey)
                if row is not None:
                    csvwriter.writerow(row)
            conn.close()

        # this suffices for small dbs, but
        # for a production big database, I imagine you would have a FileMixin that
        # does the retrieving and population even as the file object is being read
        filestream.seek(0)
        return filestream