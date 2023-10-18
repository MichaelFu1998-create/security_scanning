def _command_list(self):
        """ build the command list """
        cmd = [self.params.binary, 
                "-f", str(self.params.f), 
                "-T", str(self.params.T), 
                "-m", str(self.params.m),
                "-N", str(self.params.N),
                "-x", str(self.params.x),
                "-p", str(self.params.p),
                "-n", str(self.params.n),
                "-w", str(self.params.w),
                "-s", str(self.params.s),
               ]
        ## add ougroups
        if self.params.o:
            cmd += ["-o"]
            cmd += [",".join(self.params.o)]
        return cmd