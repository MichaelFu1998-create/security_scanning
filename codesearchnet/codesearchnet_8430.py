def scalar_write(self, address, block_count, data_file, meta_file):
        """nvme write"""
        cmd = ["nvme", "write", self.envs["DEV_PATH"], "-s 0x{:x}".format(address),
               "-c {}".format(block_count-1), "-d {}".format(data_file), "-M {}".format(meta_file),
               "-z 0x{:x}".format(block_count * self.envs["NBYTES"]),
               "-y 0x{:x}".format(block_count * self.envs["NBYTES_OOB"])]
        status, _, _ = cij.ssh.command(cmd, shell=True)
        return status