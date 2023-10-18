def _discover_via_entrypoints(self):
        """Looks for modules with amtching entry points."""
        emgr = extension.ExtensionManager(PLUGIN_EP, invoke_on_load=False)
        return ((ext.name, ext.plugin) for ext in emgr)