def delete_document(self, doc_id, conn=None):
        """
        Delete a document from index
        Returns 1 if the document was deleted, 0 if not
        """
        if conn is None:
            conn = self.redis

        return conn.execute_command(self.DEL_CMD, self.index_name, doc_id)