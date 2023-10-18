def _makeAdapter(self):
    '''
    Creates a tuple of ( Context, Adapter ) based on the options
    specified by `self.options`. The Context is the pysyncml.Context created for
    the storage location specified in `self.options`, and the Adapter is a newly
    created Adapter if a previously created one was not found.
    '''

    self._callHooks('adapter.create.init')

    # create a new pysyncml.Context. the main function that this provides is
    # to give the Adapter a storage engine to store state information across
    # synchronizations.
    context = pysyncml.Context(storage='sqlite:///%ssyncml.db' % (self.dataDir,),
                               owner=None, autoCommit=True)

    self._callHooks('adapter.create.context', context)

    # create an Adapter from the current context. this will either create
    # a new adapter, or load the current local adapter for the specified
    # context storage location. if it is new, then lots of required
    # information (such as device info) will not be set, so we need to
    # check that and specify it if missing.

    adapter = context.Adapter()

    if hasattr(self, 'serverConf') and self.serverConf.policy is not None:
      adapter.conflictPolicy = self.serverConf.policy

    if self.options.name is not None or self.appDisplay is not None:
      adapter.name = self.options.name or self.appDisplay

    # TODO: stop ignoring ``self.options.remoteUri``... (the router must first support
    #       manual routes...)
    # if self.options.remoteUri is not None:
    #   adapter.router.addRoute(self.agent.uri, self.options.remoteUri)

    if adapter.devinfo is None:
      log.info('adapter has no device info - registering new device')
    else:
      if self.options.devid is not None and self.options.devid != adapter.devinfo.devID:
        log.info('adapter has different device ID - overwriting with new device info')
        adapter.devinfo = None

    if adapter.devinfo is None:
      # setup some information about the local device, most importantly the
      # device ID, which the remote peer will use to uniquely identify this peer
      devinfoParams = dict(
        devID             = self.options.devid or self.defaultDevID,
        devType           = pysyncml.DEVTYPE_SERVER if self.options.server else \
                            pysyncml.DEVTYPE_WORKSTATION,
        manufacturerName  = 'pysyncml',
        modelName         = self.appLabel,
        softwareVersion   = pysyncml.version,
        hierarchicalSync  = self.agent.hierarchicalSync if self.agent is not None else False,
        )
      if self.devinfoParams is not None:
        devinfoParams.update(self.devinfoParams)
      adapter.devinfo = context.DeviceInfo(**devinfoParams)

    self._callHooks('adapter.create.adapter', context, adapter)

    if not self.options.server:

      # servers don't have a fixed peer; i.e. the SyncML message itself
      # defines which peer is connecting.

      if adapter.peer is None:
        if self.options.remote is None:
          self.options.remote = raw_input('SyncML remote URL: ')
          if self.options.username is None:
            self.options.username = raw_input('SyncML remote username (leave empty if none): ')
            if len(self.options.username) <= 0:
              self.options.username = None
        log.info('adapter has no remote info - registering new remote adapter')
      else:
        if self.options.remote is not None:
          if self.options.remote != adapter.peer.url \
             or self.options.username != adapter.peer.username \
             or self.options.password != adapter.peer.password:
            #or self.options.password is not None:
            log.info('adapter has invalid or rejected remote info - overwriting with new remote info')
            adapter.peer = None

      if adapter.peer is None:
        auth = None
        if self.options.username is not None:
          auth = pysyncml.NAMESPACE_AUTH_BASIC
          if self.options.password is None:
            self.options.password = getpass.getpass('SyncML remote password: ')
        # setup the remote connection parameters, if not already stored in
        # the adapter sync tables or the URL has changed.
        adapter.peer = context.RemoteAdapter(
          url      = self.options.remote,
          auth     = auth,
          username = self.options.username,
          password = self.options.password,
          )

      self._callHooks('adapter.create.peer', context, adapter, adapter.peer)

    # add a datastore attached to the URI "note". the actual value of
    # the URI is irrelevant - it is only an identifier for this item
    # synchronization channel. it must be unique within this adapter
    # and must stay consistent across synchronizations.

    # TODO: this check should be made redundant... (ie. once the
    #       implementation of Store.merge() is fixed this will
    #       become a single "addStore()" call without the check first).
    uri = self.storeParams.get('uri', self.appLabel)
    if uri in adapter.stores:
      store = adapter.stores[uri]
      store.agent = self.agent
    else:
      storeParams = dict(
        uri         = uri,
        displayName = self.options.name or self.appDisplay,
        agent       = self.agent,
        # TODO: adding this for funambol-compatibility...
        maxObjSize  = None)
      if self.storeParams is not None:
        storeParams.update(self.storeParams)
      store = adapter.addStore(context.Store(**storeParams))

    self._callHooks('adapter.create.store', context, adapter, store)

    if self.options.local:
      def locprint(msg):
        print msg
    else:
      locprint = log.info
    def showChanges(changes, prefix):
      for c in changes:
        if c.state != pysyncml.ITEM_DELETED:
          item = self.agent.getItem(c.itemID)
        else:
          item = 'Item ID %s' % (c.itemID,)
        locprint('%s  - %s: %s' % (prefix, item, pysyncml.state2string(c.state)))
    if self.options.server:
      peers = adapter.getKnownPeers()
      if len(peers) > 0:
        locprint('Pending changes to propagate:')
      else:
        locprint('No pending changes to propagate (no peers yet)')
      for peer in peers:
        for puri, pstore in peer.stores.items():
          if pstore.binding is None or pstore.binding.uri != store.uri:
            continue
          changes = list(pstore.getRegisteredChanges())
          if len(changes) <= 0:
            locprint('  Registered to peer "%s" URI "%s": (none)' % (peer.devID, puri))
          else:
            locprint('  Registered to peer "%s" URI "%s":' % (peer.devID, puri))
          showChanges(changes, '  ')
    else:
      if store.peer is None:
        locprint('No pending local changes (not associated yet).')
      else:
        changes = list(store.peer.getRegisteredChanges())
        if len(changes) <= 0:
          locprint('No pending local changes to synchronize.')
        else:
          locprint('Pending local changes:')
        showChanges(changes, '')

    self._callHooks('adapter.create.term', context, adapter)

    return (context, adapter)