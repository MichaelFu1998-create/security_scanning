def get_property_value(self, name):
        """Return the value of a property.

        The base implementation handles:

        - ``{DAV:}lockdiscovery`` and ``{DAV:}supportedlock`` using the
          associated lock manager.
        - All other *live* properties (i.e. name starts with ``{DAV:}``) are
          delegated to self.getLivePropertyValue()
        - Finally, other properties are considered *dead*, and are handled  using
          the associated property manager, if one is present.
        """
        # Return table field as property
        tableName, primKey = self.provider._split_path(self.path)
        if primKey is not None:
            ns, localName = util.split_namespace(name)
            if ns == (tableName + ":"):
                conn = self.provider._init_connection()
                fieldlist = self.provider._get_field_list(conn, tableName)
                if localName in fieldlist:
                    val = self.provider._get_field_by_primary_key(
                        conn, tableName, primKey, localName
                    )
                    conn.close()
                    return val
                conn.close()
        # else, let default implementation return supported live and dead properties
        return super(MySQLBrowserResource, self).get_property_value(name)