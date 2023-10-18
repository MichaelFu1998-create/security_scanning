def upload(self, path, progress_callback=None, finished_callback=None, error_callback=None):
        """ Create a new thread to upload a file (thread should be
        then started with start() to perform upload.)

        Args:
            path (str): Path to file

        Kwargs:
            progress_callback (func): Callback to call as file is uploaded (parameters: current, total)
            finished_callback (func): Callback to call when upload is finished
            error_callback (func): Callback to call when an error occurred (parameters: exception)

        Returns:
            :class:`Upload`. Upload thread
        """
        return Upload(
            self,
            {"upload": path},
            progress_callback = progress_callback,
            finished_callback = finished_callback,
            error_callback = error_callback
        )