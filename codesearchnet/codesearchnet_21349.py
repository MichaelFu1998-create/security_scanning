def register_plugins(self):
        """ Register plugins in Nemo instance

        - Clear routes first if asked by one plugin
        - Clear assets if asked by one plugin and replace by the last plugin registered static_folder
        - Register each plugin
            - Append plugin routes to registered routes
            - Append plugin filters to registered filters
            - Append templates directory to given namespaces
            - Append assets (CSS, JS, statics) to given resources 
            - Append render view (if exists) to Nemo.render stack
        """
        if len([plugin for plugin in self.__plugins__.values() if plugin.clear_routes]) > 0:  # Clear current routes
            self._urls = list()
            self.cached = list()

        clear_assets = [plugin for plugin in self.__plugins__.values() if plugin.clear_assets]
        if len(clear_assets) > 0 and not self.prevent_plugin_clearing_assets:  # Clear current Assets
            self.__assets__ = copy(type(self).ASSETS)
            static_path = [plugin.static_folder for plugin in clear_assets if plugin.static_folder]
            if len(static_path) > 0:
                self.static_folder = static_path[-1]

        for plugin in self.__plugins__.values():
            self._urls.extend([(url, function, methods, plugin) for url, function, methods in plugin.routes])
            self._filters.extend([(filt, plugin) for filt in plugin.filters])
            self.__templates_namespaces__.extend(
                [(namespace, directory) for namespace, directory in plugin.templates.items()]
            )
            for asset_type in self.__assets__:
                for key, value in plugin.assets[asset_type].items():
                    self.__assets__[asset_type][key] = value
            if plugin.augment:
                self.__plugins_render_views__.append(plugin)

            if hasattr(plugin, "CACHED"):
                for func in plugin.CACHED:
                    self.cached.append((getattr(plugin, func), plugin))
            plugin.register_nemo(self)