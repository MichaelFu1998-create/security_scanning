def request_object(self, address, state, object_handler,
            error_handler = None, timeout_handler = None,
            backup_state = None, timeout = timedelta(minutes=60),
            freshness_period = None, expiration_period = None,
            purge_period = None):
        """Request an object with given address and state not worse than
        `state`. The object will be taken from cache if available, and
        created/fetched otherwise. The request is asynchronous -- this metod
        doesn't return the object directly, but the `object_handler` is called
        as soon as the object is available (this may be before `request_object`
        returns and may happen in other thread). On error the `error_handler`
        will be called, and on timeout -- the `timeout_handler`.

        :Parameters:
            - `address`: address of the object requested.
            - `state`: the worst acceptable object state. When 'new' then always
              a new object will be created/fetched. 'stale' will select any
              item available in cache.
            - `object_handler`: function to be called when object is available.
              It will be called with the following arguments: address, object
              and its state.
            - `error_handler`: function to be called on object retrieval error.
              It will be called with two arguments: requested address and
              additional error information (fetcher-specific, may be
              StanzaError for XMPP objects).  If not given, then the object
              handler will be called with object set to `None` and state
              "error".
            - `timeout_handler`: function to be called on object retrieval
              timeout.  It will be called with only one argument: the requested
              address. If not given, then the `error_handler` will be called
              instead, with error details set to `None`.
            - `backup_state`: when set and object in state `state` is not
              available in the cache and object retrieval failed then object
              with this state will also be looked-up in the cache and provided
              if available.
            - `timeout`: time interval after which retrieval of the object
              should be given up.
            - `freshness_period`: time interval after which the item created
              should become 'old'.
            - `expiration_period`: time interval after which the item created
              should become 'stale'.
            - `purge_period`: time interval after which the item created
              shuld be removed from the cache.
        :Types:
            - `address`: any hashable
            - `state`: "new", "fresh", "old" or "stale"
            - `object_handler`: callable(address, value, state)
            - `error_handler`: callable(address, error_data)
            - `timeout_handler`: callable(address)
            - `backup_state`: "new", "fresh", "old" or "stale"
            - `timeout`: `timedelta`
            - `freshness_period`: `timedelta`
            - `expiration_period`: `timedelta`
            - `purge_period`: `timedelta`
        """
        self._lock.acquire()
        try:
            if state == 'stale':
                state = 'purged'
            item = self.get_item(address, state)
            if item:
                object_handler(item.address, item.value, item.state)
                return
            if not self._fetcher:
                raise TypeError("No cache fetcher defined")
            if not error_handler:
                def default_error_handler(address, _unused):
                    "Default error handler."
                    return object_handler(address, None, 'error')
                error_handler = default_error_handler
            if not timeout_handler:
                def default_timeout_handler(address):
                    "Default timeout handler."
                    return error_handler(address, None)
                timeout_handler = default_timeout_handler
            if freshness_period is None:
                freshness_period = self.default_freshness_period
            if expiration_period is None:
                expiration_period = self.default_expiration_period
            if purge_period is None:
                purge_period = self.default_purge_period

            fetcher = self._fetcher(self, address, freshness_period,
                    expiration_period, purge_period, object_handler, error_handler,
                    timeout_handler, timeout, backup_state)
            fetcher.fetch()
            self._active_fetchers.append((fetcher.timeout_time,fetcher))
            self._active_fetchers.sort()
        finally:
            self._lock.release()