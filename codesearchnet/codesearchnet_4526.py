def push_file(self, source, dest_dir):
        ''' If the source files dirpath is the same as dest_dir, a copy
        is not necessary, and nothing is done. Else a copy is made.

        Args:
            - source (string) : Path to the source file
            - dest_dir (string) : Path to the directory to which the files is to be copied

        Returns:
            - destination_path (String) : Absolute path of the destination file

        Raises:
            - FileCopyException : If file copy failed.
        '''

        local_dest = dest_dir + '/' + os.path.basename(source)

        # Only attempt to copy if the target dir and source dir are different
        if os.path.dirname(source) != dest_dir:
            try:
                shutil.copyfile(source, local_dest)
                os.chmod(local_dest, 0o777)

            except OSError as e:
                raise FileCopyException(e, self.hostname)

        return local_dest