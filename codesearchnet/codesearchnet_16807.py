def create(cls, object_type=None, object_uuid=None, **kwargs):
        """Create a new deposit identifier.

        :param object_type: The object type (Default: ``None``)
        :param object_uuid: The object UUID (Default: ``None``)
        :param kwargs: It contains the pid value.
        """
        assert 'pid_value' in kwargs
        kwargs.setdefault('status', cls.default_status)
        return super(DepositProvider, cls).create(
            object_type=object_type, object_uuid=object_uuid, **kwargs)