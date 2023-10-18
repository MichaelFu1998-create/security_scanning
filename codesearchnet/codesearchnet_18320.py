def _on_file_moved(self, event: FileSystemMovedEvent):
        """
        Called when a file in the monitored directory has been moved.

        Breaks move down into a delete and a create (which it is sometimes detected as!).
        :param event: the file system event
        """
        if not event.is_directory and self.is_data_file(event.src_path):
            delete_event = FileSystemEvent(event.src_path)
            delete_event.event_type = EVENT_TYPE_DELETED
            self._on_file_deleted(delete_event)

            create_event = FileSystemEvent(event.dest_path)
            create_event.event_type = EVENT_TYPE_CREATED
            self._on_file_created(create_event)