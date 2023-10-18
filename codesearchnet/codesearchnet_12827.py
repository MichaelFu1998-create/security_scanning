def _command_list(self):
        """ build the command list """

        ## base args
        cmd = [self.params.binary, 
                "-i", OPJ(self.workdir, self.name+".treemix.in.gz"),
                "-o", OPJ(self.workdir, self.name),
                ]

        ## addon params
        args = []
        for key, val in self.params:
            if key not in ["minmap", "binary"]:
                if key == "g":
                    if val[0]:
                        args += ["-"+key, str(val[0]), str(val[1])]
                elif key == "global_":
                    if val:
                        args += ["-"+key[:-1]]
                elif key in ["se", "global", "noss"]: 
                    if val:
                        args += ["-"+key]
                else:
                    if val:
                        args += ["-"+key, str(val)]

        return cmd+args