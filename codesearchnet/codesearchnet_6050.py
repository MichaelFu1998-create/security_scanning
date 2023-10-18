def get_member_list(self):
        """Return list of (direct) collection member names (UTF-8 byte strings).

        See DAVResource.get_member_list()
        """
        members = []
        conn = self.provider._init_connection()
        try:
            tableName, primKey = self.provider._split_path(self.path)
            if tableName is None:
                retlist = self.provider._list_tables(conn)
                for name in retlist:
                    members.append(
                        MySQLBrowserResource(
                            self.provider,
                            util.join_uri(self.path, name),
                            True,
                            self.environ,
                        )
                    )
            elif primKey is None:
                pri_key = self.provider._find_primary_key(conn, tableName)
                if pri_key is not None:
                    retlist = self.provider._list_fields(conn, tableName, pri_key)
                    for name in retlist:
                        members.append(
                            MySQLBrowserResource(
                                self.provider,
                                util.join_uri(self.path, name),
                                False,
                                self.environ,
                            )
                        )
                members.insert(
                    0,
                    MySQLBrowserResource(
                        self.provider,
                        util.join_uri(self.path, "_ENTIRE_CONTENTS"),
                        False,
                        self.environ,
                    ),
                )
        finally:
            conn.close()
        return members