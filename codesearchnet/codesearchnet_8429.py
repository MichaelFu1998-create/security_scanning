def vector_read(self, address_list, file_name=None):
        """nvm_cmd read"""
        address = ["0x{:x}".format(i) for i in address_list]
        cmd = ["nvm_cmd read", self.envs["DEV_PATH"], " ".join(address)]
        if file_name:
            cmd += ["-o {}".format(file_name)]
        status, _, _ = cij.ssh.command(cmd, shell=True)
        return status