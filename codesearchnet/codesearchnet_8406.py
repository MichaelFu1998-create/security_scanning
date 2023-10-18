def slc_erase(self, address, BE_ID=0x1, PMODE=0x0100):
        """slc erase"""
        cmd = ["NVM_CLI_BE_ID=0x%x" % BE_ID, "NVM_CLI_PMODE=0x%x" % PMODE, "nvm_cmd erase", self.envs, "0x%x" % address]
        status, _, _ = cij.ssh.command(cmd, shell=True)
        return status