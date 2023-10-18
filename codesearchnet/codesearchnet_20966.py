def run(self):
        """ Called by the thread, it runs the process.

        NEVER call this method directly. Instead call start() to start the thread.

        Before finishing the thread using this thread, call join()
        """
        queue = Queue()
        process = UploadProcess(self._connection_settings, self._room, queue, self._files)
        if self._data:
            process.add_data(self._data)
        process.start()

        if not process.is_alive():
            return

        self._uploading = True

        done = False
        while not self._abort and not done:
            if not process.is_alive():
                self._abort = True
                break

            messages = None
            try:
                data = queue.get()
                if not data:
                    done = True
                    if self._finished_callback:
                        self._finished_callback()
                elif isinstance(data, tuple):
                    sent, total = data
                    if self._progress_callback:
                        self._progress_callback(sent, total)
                else:
                    self._abort = True
                    if self._error_callback:
                        self._error_callback(data, self._room)
            except Empty:
                time.sleep(0.5)

        self._uploading = False
        if self._abort and not process.is_alive() and self._error_callback:
            self._error_callback(Exception("Upload process was killed"), self._room)

        queue.close()
        if process.is_alive():
            queue.close()
            process.terminate()
        process.join()