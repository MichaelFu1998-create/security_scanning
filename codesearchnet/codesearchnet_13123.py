def _get_binary(self):
        """ find binaries available"""

        ## check for binary
        backup_binaries = ["raxmlHPC-PTHREADS", "raxmlHPC-PTHREADS-SSE3"]

        ## check user binary first, then backups
        for binary in [self.params.binary] + backup_binaries:
            proc = subprocess.Popen(["which", self.params.binary], 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT).communicate()
            ## update the binary
            if proc:
                self.params.binary = binary

        ## if none then raise error
        if not proc[0]:
            raise Exception(BINARY_ERROR.format(self.params.binary))