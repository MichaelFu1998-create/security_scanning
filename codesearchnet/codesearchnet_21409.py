def commands2tree(self, adapter, session, commands):
    '''Consumes state.Command commands and converts them to an ET protocol tree'''

    # todo: trap errors...

    hdrcmd = commands[0]
    commands = commands[1:]

    if hdrcmd.name != constants.CMD_SYNCHDR:
      raise common.InternalError('unexpected first command "%s" (expected "%s")'
                                 % (hdrcmd.name, constants.CMD_SYNCHDR))

    if hdrcmd.version != constants.SYNCML_VERSION_1_2:
      raise common.FeatureNotSupported('unsupported SyncML version "%s"' % (hdrcmd.version,))

    xsync = ET.Element(constants.NODE_SYNCML)
    xhdr  = ET.SubElement(xsync, hdrcmd.name)
    if hdrcmd.version == constants.SYNCML_VERSION_1_2:
      ET.SubElement(xhdr, 'VerDTD').text = constants.SYNCML_DTD_VERSION_1_2
      ET.SubElement(xhdr, 'VerProto').text = hdrcmd.version

    ET.SubElement(xhdr, 'SessionID').text = hdrcmd.sessionID
    ET.SubElement(xhdr, 'MsgID').text = hdrcmd.msgID
    xsrc = ET.SubElement(xhdr, 'Source')
    ET.SubElement(xsrc, 'LocURI').text = hdrcmd.source
    if hdrcmd.sourceName is not None:
      ET.SubElement(xsrc, 'LocName').text = hdrcmd.sourceName
    xtgt = ET.SubElement(xhdr, 'Target')
    ET.SubElement(xtgt, 'LocURI').text = hdrcmd.target
    if hdrcmd.targetName is not None:
      ET.SubElement(xtgt, 'LocName').text = hdrcmd.targetName
    if hdrcmd.respUri is not None:
      ET.SubElement(xhdr, 'RespURI').text = hdrcmd.respUri

    if hdrcmd.auth is not None and not session.authAccepted:
      if hdrcmd.auth != constants.NAMESPACE_AUTH_BASIC:
        raise NotImplementedError('auth method "%s"' % (common.auth2string(hdrcmd.auth),))
      if hdrcmd.auth == constants.NAMESPACE_AUTH_BASIC:
        xcred = ET.SubElement(xhdr, 'Cred')
        xmeta = ET.SubElement(xcred, 'Meta')
        ET.SubElement(xmeta, 'Format', {'xmlns': constants.NAMESPACE_METINF}).text = 'b64'
        ET.SubElement(xmeta, 'Type', {'xmlns': constants.NAMESPACE_METINF}).text   = hdrcmd.auth
        ET.SubElement(xcred, 'Data').text = base64.b64encode(
          '%s:%s' % (adapter.peer.username, adapter.peer.password))
    if hdrcmd.maxMsgSize is not None or hdrcmd.maxObjSize is not None:
      xmeta = ET.SubElement(xhdr, 'Meta')
      if hdrcmd.maxMsgSize is not None:
        ET.SubElement(xmeta, 'MaxMsgSize', {'xmlns': constants.NAMESPACE_METINF}).text = hdrcmd.maxMsgSize
      if hdrcmd.maxObjSize is not None:
        ET.SubElement(xmeta, 'MaxObjSize', {'xmlns': constants.NAMESPACE_METINF}).text = hdrcmd.maxObjSize

    xbody = ET.SubElement(xsync, constants.NODE_SYNCBODY)

    for cmdidx, cmd in enumerate(commands):

      xcmd = ET.SubElement(xbody, cmd.name)
      if cmd.cmdID is not None:
        ET.SubElement(xcmd, 'CmdID').text = cmd.cmdID

      if cmd.name == constants.CMD_ALERT:
        ET.SubElement(xcmd, 'Data').text = str(cmd.data)
        xitem = ET.SubElement(xcmd, 'Item')
        ET.SubElement(ET.SubElement(xitem, 'Source'), 'LocURI').text = cmd.source
        ET.SubElement(ET.SubElement(xitem, 'Target'), 'LocURI').text = cmd.target
        if cmd.lastAnchor is not None \
           or cmd.nextAnchor is not None \
           or cmd.maxObjSize is not None:
          xmeta = ET.SubElement(xitem, 'Meta')
          xanch = ET.SubElement(xmeta, 'Anchor', {'xmlns': constants.NAMESPACE_METINF})
          if cmd.lastAnchor is not None:
            ET.SubElement(xanch, 'Last').text = cmd.lastAnchor
          if cmd.nextAnchor is not None:
            ET.SubElement(xanch, 'Next').text = cmd.nextAnchor
          if cmd.maxObjSize is not None:
            ET.SubElement(xmeta, 'MaxObjSize', {'xmlns': constants.NAMESPACE_METINF}).text = cmd.maxObjSize
        continue

      if cmd.name == constants.CMD_STATUS:
        ET.SubElement(xcmd, 'MsgRef').text    = cmd.msgRef
        ET.SubElement(xcmd, 'CmdRef').text    = cmd.cmdRef
        ET.SubElement(xcmd, 'Cmd').text       = cmd.statusOf
        if cmd.sourceRef is not None:
          ET.SubElement(xcmd, 'SourceRef').text = cmd.sourceRef
        if cmd.targetRef is not None:
          ET.SubElement(xcmd, 'TargetRef').text = cmd.targetRef
        ET.SubElement(xcmd, 'Data').text      = cmd.statusCode
        if cmd.nextAnchor is not None or cmd.lastAnchor is not None:
          xdata = ET.SubElement(ET.SubElement(xcmd, 'Item'), 'Data')
          xanch = ET.SubElement(xdata, 'Anchor', {'xmlns': constants.NAMESPACE_METINF})
          if cmd.lastAnchor is not None:
            ET.SubElement(xanch, 'Last').text = cmd.lastAnchor
          if cmd.nextAnchor is not None:
            ET.SubElement(xanch, 'Next').text = cmd.nextAnchor
        # NOTE: this is NOT standard SyncML...
        if cmd.errorCode is not None or cmd.errorMsg is not None:
          xerr = ET.SubElement(xcmd, 'Error')
          if cmd.errorCode is not None:
            ET.SubElement(xerr, 'Code').text = cmd.errorCode
          if cmd.errorMsg is not None:
            ET.SubElement(xerr, 'Message').text = cmd.errorMsg
          if cmd.errorTrace is not None:
            ET.SubElement(xerr, 'Trace').text = cmd.errorTrace
        continue

      if cmd.name in [constants.CMD_GET, constants.CMD_PUT]:
        ET.SubElement(ET.SubElement(xcmd, 'Meta'), 'Type',
                      {'xmlns': constants.NAMESPACE_METINF}).text = cmd.type
        if cmd.source is not None or cmd.target is not None or cmd.data:
          xitem = ET.SubElement(xcmd, 'Item')
        if cmd.source is not None:
          xsrc = ET.SubElement(xitem, 'Source')
          ET.SubElement(xsrc, 'LocURI').text  = cmd.source
          ET.SubElement(xsrc, 'LocName').text = cmd.source
        if cmd.target is not None:
          xtgt = ET.SubElement(xitem, 'Target')
          ET.SubElement(xtgt, 'LocURI').text  = cmd.target
          ET.SubElement(xtgt, 'LocName').text = cmd.target
        if cmd.data is not None:
          if isinstance(cmd.data, basestring):
            ET.SubElement(xitem, 'Data').text = cmd.data
          else:
            ET.SubElement(xitem, 'Data').append(cmd.data)
        continue

      if cmd.name == constants.CMD_RESULTS:
        ET.SubElement(xcmd, 'MsgRef').text    = cmd.msgRef
        ET.SubElement(xcmd, 'CmdRef').text    = cmd.cmdRef
        ET.SubElement(ET.SubElement(xcmd, 'Meta'), 'Type',
                      {'xmlns': constants.NAMESPACE_METINF}).text = cmd.type
        xitem = ET.SubElement(xcmd, 'Item')
        xsrc = ET.SubElement(xitem, 'Source')
        ET.SubElement(xsrc, 'LocURI').text  = cmd.source
        ET.SubElement(xsrc, 'LocName').text = cmd.source
        if cmd.data is not None:
          if isinstance(cmd.data, basestring):
            ET.SubElement(xitem, 'Data').text = cmd.data
          else:
            ET.SubElement(xitem, 'Data').append(cmd.data)
        continue

      if cmd.name == constants.CMD_SYNC:
        ET.SubElement(ET.SubElement(xcmd, 'Source'), 'LocURI').text = cmd.source
        ET.SubElement(ET.SubElement(xcmd, 'Target'), 'LocURI').text = cmd.target
        if cmd.noc is not None:
          ET.SubElement(xcmd, 'NumberOfChanges').text = cmd.noc
        if cmd.data is not None:
          for scmd in cmd.data:
            xscmd = ET.SubElement(xcmd, scmd.name)
            if scmd.cmdID is not None:
              ET.SubElement(xscmd, 'CmdID').text = scmd.cmdID
            if scmd.type is not None or \
              ( scmd.format is not None and scmd.format != constants.FORMAT_AUTO ):
              xsmeta = ET.SubElement(xscmd, 'Meta')
              # todo: implement auto encoding determination...
              #       (the current implementation just lets XML encoding do it,
              #        which is for most things good enough, but not so good
              #        for sequences that need a large amount escaping such as
              #        binary data...)
              if scmd.format is not None and scmd.format != constants.FORMAT_AUTO:
                ET.SubElement(xsmeta, 'Format', {'xmlns': constants.NAMESPACE_METINF}).text = scmd.format
              if scmd.type is not None:
                ET.SubElement(xsmeta, 'Type', {'xmlns': constants.NAMESPACE_METINF}).text = scmd.type
            xsitem = ET.SubElement(xscmd, 'Item')
            if scmd.source is not None:
              ET.SubElement(ET.SubElement(xsitem, 'Source'), 'LocURI').text = scmd.source
            if scmd.sourceParent is not None:
              ET.SubElement(ET.SubElement(xsitem, 'SourceParent'), 'LocURI').text = scmd.sourceParent
            if scmd.target is not None:
              ET.SubElement(ET.SubElement(xsitem, 'Target'), 'LocURI').text = scmd.target
            if scmd.targetParent is not None:
              ET.SubElement(ET.SubElement(xsitem, 'TargetParent'), 'LocURI').text = scmd.targetParent
            if scmd.data is not None:
              if isinstance(scmd.data, basestring):
                ET.SubElement(xsitem, 'Data').text = scmd.data
              else:
                ET.SubElement(xsitem, 'Data').append(scmd.data)
        continue

      if cmd.name == constants.CMD_MAP:
        ET.SubElement(ET.SubElement(xcmd, 'Source'), 'LocURI').text = cmd.source
        ET.SubElement(ET.SubElement(xcmd, 'Target'), 'LocURI').text = cmd.target
        if cmd.sourceItem is not None or cmd.targetItem is not None:
          xitem = ET.SubElement(xcmd, constants.CMD_MAPITEM)
          if cmd.sourceItem is not None:
            ET.SubElement(ET.SubElement(xitem, 'Source'), 'LocURI').text = cmd.sourceItem
          if cmd.targetItem is not None:
            ET.SubElement(ET.SubElement(xitem, 'Target'), 'LocURI').text = cmd.targetItem
        continue

      if cmd.name == constants.CMD_FINAL:
        if cmdidx + 1 < len(commands):
          raise common.InternalError('command "%s" not at tail end of commands' % (cmd.name,))
        continue

      raise common.InternalError('unexpected command "%s"' % (cmd.name,))

    return xsync