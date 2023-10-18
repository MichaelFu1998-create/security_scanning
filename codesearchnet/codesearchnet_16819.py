def delete(self, pid, record, key):
        """Handle DELETE deposit file.

        Permission required: `update_permission_factory`.

        :param pid: Pid object (from url).
        :param record: Record object resolved from the pid.
        :param key: Unique identifier for the file in the deposit.
        """
        try:
            del record.files[str(key)]
            record.commit()
            db.session.commit()
            return make_response('', 204)
        except KeyError:
            abort(404, 'The specified object does not exist or has already '
                  'been deleted.')