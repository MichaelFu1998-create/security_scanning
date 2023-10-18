def watch(self):
        """
            Watches directory for changes
        """
        wm = pyinotify.WatchManager()
        self.notifier = pyinotify.Notifier(wm, default_proc_fun=self.callback)
        wm.add_watch(self.directory, pyinotify.ALL_EVENTS)
        try:
            self.notifier.loop()
        except (KeyboardInterrupt, AttributeError):
            print_notification("Stopping")
        finally:
            self.notifier.stop()
            self.terminate_processes()