def unregister_hook(self, func):
        """ Unregisters a hook. For further explanation, please have a look at ``register_hook``. """
        if func in self.hooks:
            self.hooks.remove(func)