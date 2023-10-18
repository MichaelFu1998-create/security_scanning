def vblk_write(self, address, meta=False):
        """nvm_vblk write"""
        cmd = list()
        if meta:
            cmd.append("NVM_CLI_META_MODE=1")
        cmd += ["nvm_vblk write", self.envs["DEV_PATH"], "0x%x" % address]
        status, _, _ = cij.ssh.command(cmd, shell=True)
        return status