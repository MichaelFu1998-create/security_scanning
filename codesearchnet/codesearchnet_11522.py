def play(self, song):
        """Play a new song from a Pandora model

        Returns once the stream starts but does not shut down the remote audio
        output backend process. Calls the input callback when the user has
        input.
        """
        self._callbacks.play(song)
        self._load_track(song)
        time.sleep(2)  # Give the backend time to load the track

        while True:
            try:
                self._callbacks.pre_poll()
                self._ensure_started()
                self._loop_hook()

                readers, _, _ = select.select(
                    self._get_select_readers(), [], [], 1)

                for handle in readers:
                    if handle.fileno() == self._control_fd:
                        self._callbacks.input(handle.readline().strip(), song)
                    else:
                        value = self._read_from_process(handle)
                        if self._player_stopped(value):
                            return
            finally:
                self._callbacks.post_poll()