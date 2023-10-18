def load(self, prefix=None, depth=None):
        """
        Return a dictionary of settings loaded from etcd.

        """
        prefix = prefix or self.prefix
        prefix = '/' + prefix.strip('/') + '/'
        if depth is None:
            depth = self.inherit_depth

        if not self.configured:
            log.debug("etcd not available")
            return

        if self.watching:
            log.info("Starting watcher for %r", prefix)
            self.start_watching()

        log.info("Loading from etcd %r", prefix)
        try:
            result = self.client.get(prefix)
        except self.module.EtcdKeyNotFound:
            result = None
        if not result:
            log.info("No configuration found")
            return {}

        # Iterate over the returned keys from etcd
        update = {}
        for item in result.children:
            key = item.key
            value = item.value
            # Try to parse them as JSON strings, just in case it works
            try:
                value = pytool.json.from_json(value)
            except:
                pass

            # Make the key lower-case if we're not case-sensitive
            if not self.case_sensitive:
                key = key.lower()

            # Strip off the prefix that we're using
            if key.startswith(prefix):
                key = key[len(prefix):]

            # Store the key/value to update the config
            update[key] = value

        # Access cached settings directly to avoid recursion
        inherited = Config().settings.get(self.inherit_key,
                update.get(self.inherit_key, None))
        if depth > 0 and inherited:
            log.info("    ... inheriting ...")
            inherited = self.load(inherited, depth - 1) or {}
            inherited.update(update)
            update = inherited

        return update