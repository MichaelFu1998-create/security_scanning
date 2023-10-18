def watch_files(self):
        """watch files for changes, if changed, rebuild blog. this thread
        will quit if the main process ends"""

        try:
            while 1:
                sleep(1)  # check every 1s

                try:
                    files_stat = self.get_files_stat()
                except SystemExit:
                    logger.error("Error occurred, server shut down")
                    self.shutdown_server()

                if self.files_stat != files_stat:
                    logger.info("Changes detected, start rebuilding..")

                    try:
                        generator.re_generate()
                        global _root
                        _root = generator.root
                    except SystemExit:  # catch sys.exit, it means fatal error
                        logger.error("Error occurred, server shut down")
                        self.shutdown_server()

                    self.files_stat = files_stat  # update files' stat
        except KeyboardInterrupt:
            # I dont know why, but this exception won't be catched
            # because absolutly each KeyboardInterrupt is catched by
            # the server thread, which will terminate this thread the same time
            logger.info("^C received, shutting down watcher")
            self.shutdown_watcher()