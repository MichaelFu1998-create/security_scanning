def _add_document(self, doc_id, conn=None, nosave=False, score=1.0, payload=None,
                      replace=False, partial=False, language=None, **fields):
        """ 
        Internal add_document used for both batch and single doc indexing 
        """
        if conn is None:
            conn = self.redis

        if partial:
            replace = True

        args = [self.ADD_CMD, self.index_name, doc_id, score]
        if nosave:
            args.append('NOSAVE')
        if payload is not None:
            args.append('PAYLOAD')
            args.append(payload)
        if replace:
            args.append('REPLACE')
            if partial:
                args.append('PARTIAL')
        if language:
            args += ['LANGUAGE', language]
        args.append('FIELDS')
        args += list(itertools.chain(*fields.items()))
        return conn.execute_command(*args)