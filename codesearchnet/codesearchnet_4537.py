def push_file(self, local_source, remote_dir):
        ''' Transport a local file to a directory on a remote machine

        Args:
            - local_source (string): Path
            - remote_dir (string): Remote path

        Returns:
            - str: Path to copied file on remote machine

        Raises:
            - BadScriptPath : if script path on the remote side is bad
            - BadPermsScriptPath : You do not have perms to make the channel script dir
            - FileCopyException : FileCopy failed.

        '''
        remote_dest = remote_dir + '/' + os.path.basename(local_source)

        try:
            self.makedirs(remote_dir, exist_ok=True)
        except IOError as e:
            logger.exception("Pushing {0} to {1} failed".format(local_source, remote_dir))
            if e.errno == 2:
                raise BadScriptPath(e, self.hostname)
            elif e.errno == 13:
                raise BadPermsScriptPath(e, self.hostname)
            else:
                logger.exception("File push failed due to SFTP client failure")
                raise FileCopyException(e, self.hostname)
        try:
            self.sftp_client.put(local_source, remote_dest, confirm=True)
            # Set perm because some systems require the script to be executable
            self.sftp_client.chmod(remote_dest, 0o777)
        except Exception as e:
            logger.exception("File push from local source {} to remote destination {} failed".format(
                local_source, remote_dest))
            raise FileCopyException(e, self.hostname)

        return remote_dest