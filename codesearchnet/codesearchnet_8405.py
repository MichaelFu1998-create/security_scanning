def vblk_erase(self, address):
        """nvm_vblk erase"""
        cmd = ["nvm_vblk erase", self.envs, "0x%x" % address]
        status, _, _ = cij.ssh.command(cmd, shell=True)
        return status