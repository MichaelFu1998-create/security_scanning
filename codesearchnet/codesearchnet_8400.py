def get_chunk_information(self, chk, lun, chunk_name):
        """Get chunk information"""
        cmd = ["nvm_cmd rprt_lun", self.envs,
               "%d %d > %s" % (chk, lun, chunk_name)]
        status, _, _ = cij.ssh.command(cmd, shell=True)
        return status