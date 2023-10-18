def tree2commands(self, adapter, session, lastcmds, xsync):
    '''Consumes an ET protocol tree and converts it to state.Command commands'''

    # do some preliminary sanity checks...
    # todo: do i really want to be using assert statements?...

    assert xsync.tag == constants.NODE_SYNCML
    assert len(xsync) == 2
    assert xsync[0].tag == constants.CMD_SYNCHDR
    assert xsync[1].tag == constants.NODE_SYNCBODY

    version = xsync[0].findtext('VerProto')
    if version != constants.SYNCML_VERSION_1_2:
      raise common.FeatureNotSupported('unsupported SyncML version "%s" (expected "%s")' \
                                       % (version, constants.SYNCML_VERSION_1_2))
    verdtd = xsync[0].findtext('VerDTD')
    if verdtd != constants.SYNCML_DTD_VERSION_1_2:
      raise common.FeatureNotSupported('unsupported SyncML DTD version "%s" (expected "%s")' \
                                       % (verdtd, constants.SYNCML_DTD_VERSION_1_2))

    ret = self.initialize(adapter, session, xsync)
    hdrcmd = ret[0]

    if session.isServer:
      log.debug('received request SyncML message from "%s" (s%s.m%s)',
                hdrcmd.target, hdrcmd.sessionID, hdrcmd.msgID)
    else:
      log.debug('received response SyncML message from "%s" (s%s.m%s)',
                lastcmds[0].target, lastcmds[0].sessionID, lastcmds[0].msgID)

    try:
      return self._tree2commands(adapter, session, lastcmds, xsync, ret)
    except Exception, e:
      if not session.isServer:
        raise
      # TODO: make this configurable as to whether or not any error
      #       is sent back to the peer as a SyncML "standardized" error
      #       status...
      code = '%s.%s' % (e.__class__.__module__, e.__class__.__name__)
      msg  = ''.join(traceback.format_exception_only(type(e), e)).strip()
      log.exception('failed while interpreting command tree: %s', msg)
      # TODO: for some reason, the active exception is not being logged...
      return [
        hdrcmd,
        state.Command(
          name       = constants.CMD_STATUS,
          cmdID      = '1',
          msgRef     = session.pendingMsgID,
          cmdRef     = 0,
          sourceRef  = xsync[0].findtext('Source/LocURI'),
          targetRef  = xsync[0].findtext('Target/LocURI'),
          statusOf   = constants.CMD_SYNCHDR,
          statusCode = constants.STATUS_COMMAND_FAILED,
          errorCode  = code,
          errorMsg   = msg,
          errorTrace = ''.join(traceback.format_exception(type(e), e, sys.exc_info()[2])),
          ),
        state.Command(name=constants.CMD_FINAL)]