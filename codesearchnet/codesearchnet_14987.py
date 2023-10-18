def register_service(self, url, data=None, overwrite=True):
        """
        Implementation of :meth:`twitcher.api.IRegistry.register_service`.
        """
        data = data or {}

        args = dict(data)
        args['url'] = url
        service = Service(**args)
        service = self.store.save_service(service, overwrite=overwrite)
        return service.params