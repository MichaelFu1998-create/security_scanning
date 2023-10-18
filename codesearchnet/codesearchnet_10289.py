def prehook(self, **kwargs):
        """Launch local smpd."""
        cmd = ['smpd', '-s']
        logger.info("Starting smpd: "+" ".join(cmd))
        rc = subprocess.call(cmd)
        return rc