def get(self, pid, record, key, version_id, **kwargs):
        """Get file.

        Permission required: `read_permission_factory`.

        :param pid: Pid object (from url).
        :param record: Record object resolved from the pid.
        :param key: Unique identifier for the file in the deposit.
        :param version_id: File version. Optional. If no version is provided,
            the last version is retrieved.
        :returns: the file content.
        """
        try:
            obj = record.files[str(key)].get_version(version_id=version_id)
            return self.make_response(
                obj=obj or abort(404), pid=pid, record=record)
        except KeyError:
            abort(404)