def stage_out(self, file, executor):
        """Transport the file from the local filesystem to the remote Globus endpoint.

        This function returns a DataFuture.

        Args:
            - self
            - file (File) - file to stage out
            - executor (str) - Which executor the file is going to be staged out from.
                                If the executor argument is not specified for a file
                                with the 'globus' scheme, the file will be staged in to
                                the first executor with the "globus" key in a config.
        """

        if file.scheme == 'http' or file.scheme == 'https':
            raise Exception('HTTP/HTTPS file staging out is not supported')
        elif file.scheme == 'ftp':
            raise Exception('FTP file staging out is not supported')
        elif file.scheme == 'globus':
            globus_ep = self._get_globus_endpoint(executor)
            stage_out_app = self._globus_stage_out_app()
            return stage_out_app(globus_ep, inputs=[file])
        else:
            raise Exception('Staging out with unknown file scheme {} is not supported'.format(file.scheme))