def play_sync(self):
        """
        Play the video and block whilst the video is playing
        """
        self.play()
        logger.info("Playing synchronously")
        try:
            time.sleep(0.05)
            logger.debug("Wait for playing to start")
            while self.is_playing():
                time.sleep(0.05)
        except DBusException:
            logger.error(
                "Cannot play synchronously any longer as DBus calls timed out."
            )