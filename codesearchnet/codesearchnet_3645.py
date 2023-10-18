def context(self):
        """ Convenient access to shared context """
        plugin_context_name = str(type(self))
        if plugin_context_name not in self.manticore.context:
            self.manticore.context[plugin_context_name] = {}
        return self.manticore.context[plugin_context_name]