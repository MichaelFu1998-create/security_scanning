def put(self, pid, record):
        """Handle the sort of the files through the PUT deposit files.

        Expected input in body PUT:

        .. code-block:: javascript

            [
                {
                    "id": 1
                },
                {
                    "id": 2
                },
                ...
            }

        Permission required: `update_permission_factory`.

        :param pid: Pid object (from url).
        :param record: Record object resolved from the pid.
        :returns: The files.
        """
        try:
            ids = [data['id'] for data in json.loads(
                request.data.decode('utf-8'))]
        except KeyError:
            raise WrongFile()

        record.files.sort_by(*ids)
        record.commit()
        db.session.commit()
        return self.make_response(obj=record.files, pid=pid, record=record)