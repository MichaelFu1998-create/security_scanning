def stage_in(self, file, executor):
        """Transport the file from the input source to the executor.

        This function returns a DataFuture.

        Args:
            - self
            - file (File) : file to stage in
            - executor (str) : an executor the file is going to be staged in to.
                                If the executor argument is not specified for a file
                                with 'globus' scheme, the file will be staged in to
                                the first executor with the "globus" key in a config.
        """

        if file.scheme == 'ftp':
            working_dir = self.dfk.executors[executor].working_dir
            stage_in_app = self._ftp_stage_in_app(executor=executor)
            app_fut = stage_in_app(working_dir, outputs=[file])
            return app_fut._outputs[0]
        elif file.scheme == 'http' or file.scheme == 'https':
            working_dir = self.dfk.executors[executor].working_dir
            stage_in_app = self._http_stage_in_app(executor=executor)
            app_fut = stage_in_app(working_dir, outputs=[file])
            return app_fut._outputs[0]
        elif file.scheme == 'globus':
            globus_ep = self._get_globus_endpoint(executor)
            stage_in_app = self._globus_stage_in_app()
            app_fut = stage_in_app(globus_ep, outputs=[file])
            return app_fut._outputs[0]
        else:
            raise Exception('Staging in with unknown file scheme {} is not supported'.format(file.scheme))