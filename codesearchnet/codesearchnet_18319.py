def _on_file_deleted(self, event: FileSystemEvent):
        """
        Called when a file in the monitored directory has been deleted.
        :param event: the file system event
        """
        if not event.is_directory and self.is_data_file(event.src_path):
            assert event.src_path in self._origin_mapped_data
            del(self._origin_mapped_data[event.src_path])
            self.notify_listeners(FileSystemChange.DELETE)