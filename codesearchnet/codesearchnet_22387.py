def prepare(self):
        """
        Called when builder run collect files in builder group

        :rtype: list[static_bundle.files.StaticFileResult]
        """
        result_files = self.collect_files()
        chain = self.prepare_handlers_chain
        if chain is None:
            # default handlers
            chain = [
                LessCompilerPrepareHandler()
            ]
        for prepare_handler in chain:
            result_files = prepare_handler.prepare(result_files, self)
        return result_files