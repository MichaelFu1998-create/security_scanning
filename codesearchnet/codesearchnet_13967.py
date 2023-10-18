def close(self):
        
        """Commits any pending transactions and closes the database.
        """
        
        self._con.commit()
        self._cur.close()
        self._con.close()