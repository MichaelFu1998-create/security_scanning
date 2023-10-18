def getdevice_by_uuid(uuid):
    """
    Get a HDD device by uuid

    Example::

        from burlap.disk import getdevice_by_uuid

        device = getdevice_by_uuid("356fafdc-21d5-408e-a3e9-2b3f32cb2a8c")
        if device:
            mount(device,'/mountpoint')
    """
    with settings(hide('running', 'warnings', 'stdout'), warn_only=True):
        res = run_as_root('blkid -U %s' % uuid)

        if not res.succeeded:
            return None

        return res