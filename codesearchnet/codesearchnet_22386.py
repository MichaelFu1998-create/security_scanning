def add_prepare_handler(self, prepare_handlers):
        """
        Add prepare handler to bundle

        :type: prepare_handler: static_bundle.handlers.AbstractPrepareHandler
        """
        if not isinstance(prepare_handlers, static_bundle.BUNDLE_ITERABLE_TYPES):
            prepare_handlers = [prepare_handlers]
        if self.prepare_handlers_chain is None:
            self.prepare_handlers_chain = []
        for handler in prepare_handlers:
            self.prepare_handlers_chain.append(handler)