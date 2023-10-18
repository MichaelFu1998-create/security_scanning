def put(self, pid, record, key):
        """Handle the file rename through the PUT deposit file.

        Permission required: `update_permission_factory`.

        :param pid: Pid object (from url).
        :param record: Record object resolved from the pid.
        :param key: Unique identifier for the file in the deposit.
        """
        try:
            data = json.loads(request.data.decode('utf-8'))
            new_key = data['filename']
        except KeyError:
            raise WrongFile()
        new_key_secure = secure_filename(new_key)
        if not new_key_secure or new_key != new_key_secure:
            raise WrongFile()
        try:
            obj = record.files.rename(str(key), new_key_secure)
        except KeyError:
            abort(404)
        record.commit()
        db.session.commit()
        return self.make_response(obj=obj, pid=pid, record=record)