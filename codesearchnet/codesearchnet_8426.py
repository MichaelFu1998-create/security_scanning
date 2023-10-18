def s20_to_gen(self, pugrp, punit, chunk, sectr):
        """S20 unit to generic address"""
        cmd = ["nvm_addr s20_to_gen", self.envs["DEV_PATH"],
               "%d %d %d %d" % (pugrp, punit, chunk, sectr)]
        status, stdout, _ = cij.ssh.command(cmd, shell=True)
        if status:
            raise RuntimeError("cij.liblight.s20_to_gen: cmd fail")

        return int(re.findall(r"val: ([0-9a-fx]+)", stdout)[0], 16)