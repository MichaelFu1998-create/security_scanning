def run(self):
        """ Called by the thread, it runs the process.

        NEVER call this method directly. Instead call start() to start the thread.

        To stop, call stop(), and then join()
        """

        if self._live:
            self._use_process = True

        self._abort = False
        campfire = self._room.get_campfire()

        if self._live:
            process = LiveStreamProcess(campfire.get_connection().get_settings(), self._room.id)
        else:
            process = StreamProcess(campfire.get_connection().get_settings(), self._room.id, pause=self._pause)

        if not self._use_process:
            process.set_callback(self.incoming)

        if self._use_process:
            queue = Queue()
            process.set_queue(queue)
            process.start()
            if not process.is_alive():
                return

        self._streaming = True

        while not self._abort:
            if self._use_process:
                if not process.is_alive():
                    self._abort = True
                    break

                try:
                    incoming = queue.get_nowait()
                    if isinstance(incoming, list):
                        self.incoming(incoming)
                    elif isinstance(incoming, Exception):
                        self._abort = True
                        if self._error_callback:
                            self._error_callback(incoming, self._room)

                except Empty:
                    time.sleep(self._pause)
                    pass
            else:
                process.fetch()
                time.sleep(self._pause)

        self._streaming = False
        if self._use_process and self._abort and not process.is_alive() and self._error_callback:
            self._error_callback(Exception("Streaming process was killed"), self._room)

        if self._use_process:
            queue.close()
            if process.is_alive():
                process.stop()
                process.terminate()
            process.join()