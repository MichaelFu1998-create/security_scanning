def init_repo(self, gitdir):
        """
        Insert hook into the repo
        """

        hooksdir = os.path.join(gitdir, 'hooks')
        content = postreceive_template % {
            'client': self.client,
            'bucket': self.bucket,
            's3cfg': self.s3cfg,
            'prefix': self.prefix
            }

        postrecv_filename =os.path.join(hooksdir, 'post-receive')
        with open(postrecv_filename,'w') as fd:
            fd.write(content)

        self.make_hook_executable(postrecv_filename)
        print("Wrote to", postrecv_filename)