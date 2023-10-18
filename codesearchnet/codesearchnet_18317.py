def _on_file_created(self, event: FileSystemEvent):
        """
        Called when a file in the monitored directory has been created.
        :param event: the file system event
        """
        if not event.is_directory and self.is_data_file(event.src_path):
            assert event.src_path not in self._origin_mapped_data
            self._origin_mapped_data[event.src_path] = self.no_error_extract_data_from_file(event.src_path)
            self.notify_listeners(FileSystemChange.CREATE)