def get(self, pid, record):
        """Get files.

        Permission required: `read_permission_factory`.

        :param pid: Pid object (from url).
        :param record: Record object resolved from the pid.
        :returns: The files.
        """
        return self.make_response(obj=record.files, pid=pid, record=record)