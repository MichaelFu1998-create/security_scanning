def _load_worker_plugin_with_module(self, module, version):
        """Instantiates worker plugins that have requsite properties.

        The required properties are:
        * must have PLUGIN_EP entrypoint registered (or it wouldn't be in the
          list)
        * must have class attribute versions (list) of supported RPC versions
        * must subclass QuarkAsyncPluginBase
        """
        classes = inspect.getmembers(module, inspect.isclass)
        loaded = 0
        for cls_name, cls in classes:
            if hasattr(cls, 'versions'):
                if version not in cls.versions:
                    continue
            else:
                continue
            if issubclass(cls, base_worker.QuarkAsyncPluginBase):
                LOG.debug("Loading plugin %s" % cls_name)
                plugin = cls()
                self.plugins.append(plugin)
                loaded += 1
        LOG.debug("Found %d possible plugins and loaded %d" %
                  (len(classes), loaded))