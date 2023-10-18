def post(self, pid, record):
        """Handle POST deposit files.

        Permission required: `update_permission_factory`.

        :param pid: Pid object (from url).
        :param record: Record object resolved from the pid.
        """
        # load the file
        uploaded_file = request.files['file']
        # file name
        key = secure_filename(
            request.form.get('name') or uploaded_file.filename
        )
        # check if already exists a file with this name
        if key in record.files:
            raise FileAlreadyExists()
        # add it to the deposit
        record.files[key] = uploaded_file.stream
        record.commit()
        db.session.commit()
        return self.make_response(
            obj=record.files[key].obj, pid=pid, record=record, status=201)