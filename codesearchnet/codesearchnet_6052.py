def get_property_names(self, is_allprop):
        """Return list of supported property names in Clark Notation.

        Return supported live and dead properties. (See also DAVProvider.get_property_names().)

        In addition, all table field names are returned as properties.
        """
        # Let default implementation return supported live and dead properties
        propNames = super(MySQLBrowserResource, self).get_property_names(is_allprop)
        # Add fieldnames as properties
        tableName, primKey = self.provider._split_path(self.path)
        if primKey is not None:
            conn = self.provider._init_connection()
            fieldlist = self.provider._get_field_list(conn, tableName)
            for fieldname in fieldlist:
                propNames.append("{%s:}%s" % (tableName, fieldname))
            conn.close()
        return propNames