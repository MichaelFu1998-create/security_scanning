def close(self):
        """Close the connection."""
        try:
            self.conn.close()
            self.logger.debug("Close connect succeed.")
        except pymssql.Error as e:
            self.unknown("Close connect error: %s" % e)