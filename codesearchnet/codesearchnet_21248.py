def Adapter(self, **kw):
    '''
    .. TODO:: move this documentation into model/adapter.py?...

    The Adapter constructor supports the following parameters:

    :param devID:

      sets the local adapter\'s device identifier. For servers, this
      should be the externally accessible URL that launches the SyncML
      transaction, and for clients this should be a unique ID, such as
      the IMEI number (for mobile phones). If not specified, it will
      be defaulted to the `devID` of the `devinfo` object. If it
      cannot be loaded from the database or from the `devinfo`, then
      it must be provided before any synchronization can begin.

    :param name:

      sets the local adapter\'s device name - usually a human-friendly
      description of this SyncML\'s function.

    :param devinfo:

      sets the local adapter :class:`pysyncml.devinfo.DeviceInfo`.  If
      not specified, it will be auto-loaded from the database. If it
      cannot be loaded from the database, then it must be provided
      before any synchronization can begin.

    :param peer:

      TODO: document...

    :param maxGuidSize:

      TODO: document...

    :param maxMsgSize:

      TODO: document...

    :param maxObjSize:

      TODO: document...

    :param conflictPolicy:

      sets the default conflict handling policy for this adapter,
      and can be overriden on a per-store basis (applies only when
      operating as the server role).

    '''
    try:
      ret = self._model.Adapter.q(isLocal=True).one()
      for k, v in kw.items():
        setattr(ret, k, v)
    except NoResultFound:
      ret = self._model.Adapter(**kw)
      ret.isLocal = True
      self._model.session.add(ret)
      if ret.devID is not None:
        self._model.session.flush()
    ret.context       = self
    # todo: is this really the best place to do this?...
    ret.router        = self.router or router.Router(ret)
    ret.protocol      = self.protocol or protocol.Protocol(ret)
    ret.synchronizer  = self.synchronizer or synchronizer.Synchronizer(ret)
    ret.codec         = self.codec or 'xml'
    if isinstance(ret.codec, basestring):
      ret.codec = codec.Codec.factory(ret.codec)
    if ret.devID is not None:
      peers = ret.getKnownPeers()
      if len(peers) == 1 and peers[0].url is not None:
        ret._peer = peers[0]
    return ret