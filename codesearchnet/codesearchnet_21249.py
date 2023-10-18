def RemoteAdapter(self, **kw):
    '''
    .. TODO:: move this documentation into model/adapter.py?...

    The RemoteAdapter constructor supports the following parameters:

    :param url:

      specifies the URL that this remote SyncML server can be reached
      at. The URL must be a fully-qualified URL.

    :param auth:

      set what kind of authentication scheme to use, which generally is
      one of the following values:

        **None**:

          indicates no authentication is required.

        **pysyncml.NAMESPACE_AUTH_BASIC**:

          specifies to use "Basic-Auth" authentication scheme.

        **pysyncml.NAMESPACE_AUTH_MD5**:

          specifies to use MD5 "Digest-Auth" authentication scheme.
          NOTE: this may not be implemented yet...

    :param username:

      if the `auth` is not ``None``, then the username to authenticate
      as must be provided via this parameter.

    :param password:

      if the `auth` is not ``None``, then the password to authenticate
      with must be provided via this parameter.

    '''
    # TODO: is this really the right way?...
    ret = self._model.Adapter(isLocal=False, **kw)
    self._model.session.add(ret)
    if ret.devID is not None:
      self._model.session.flush()
    return ret