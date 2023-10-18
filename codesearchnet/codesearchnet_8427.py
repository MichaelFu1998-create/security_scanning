def gen_to_dev(self, address):
        """Generic address to device address"""
        cmd = ["nvm_addr gen2dev", self.envs["DEV_PATH"], "0x{:x}".format(address)]
        status, stdout, _ = cij.ssh.command(cmd, shell=True)
        if status:
            raise RuntimeError("cij.liblight.gen_to_dev: cmd fail")

        return int(re.findall(r"dev: ([0-9a-fx]+)", stdout)[0], 16)