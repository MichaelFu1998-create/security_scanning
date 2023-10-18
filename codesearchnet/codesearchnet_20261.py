def _run(self, cmd):
        """
        Helper function to run commands

        Parameters
        ----------
        cmd : list
              Arguments to git command
        """

        # This is here in case the .gitconfig is not accessible for
        # some reason. 
        environ = os.environ.copy() 

        environ['GIT_COMMITTER_NAME'] = self.fullname
        environ['GIT_COMMITTER_EMAIL'] = self.email 
        environ['GIT_AUTHOR_NAME'] = self.fullname
        environ['GIT_AUTHOR_EMAIL'] = self.email 

        cmd = [pipes.quote(c) for c in cmd]
        cmd = " ".join(['/usr/bin/git'] + cmd)
        cmd += "; exit 0"
        #print("Running cmd", cmd)
        try:
            output = subprocess.check_output(cmd,
                                             stderr=subprocess.STDOUT,
                                             shell=True,
                                             env=environ)
        except subprocess.CalledProcessError as e:
            output = e.output

        output = output.decode('utf-8')
        output = output.strip()
        # print("Output of command", output)
        return output