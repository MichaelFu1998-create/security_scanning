def trash(self, file) :
        """
        Trash a file in the appropriate trash directory.
        If the file belong to the same volume of the trash home directory it
        will be trashed in the home trash directory.
        Otherwise it will be trashed in one of the relevant volume trash
        directories.

        Each volume can have two trash directories, they are
            - $volume/.Trash/$uid
            - $volume/.Trash-$uid

        Firstly the software attempt to trash the file in the first directory
        then try to trash in the second trash directory.
        """

        if self._should_skipped_by_specs(file):
            self.reporter.unable_to_trash_dot_entries(file)
            return

        volume_of_file_to_be_trashed = self.volume_of_parent(file)
        self.reporter.volume_of_file(volume_of_file_to_be_trashed)
        candidates = self._possible_trash_directories_for(
                        volume_of_file_to_be_trashed)

        self.try_trash_file_using_candidates(file,
                                             volume_of_file_to_be_trashed,
                                             candidates)