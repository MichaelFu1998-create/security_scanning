def sys_rt_sigaction(self, signum, act, oldact):
        """Wrapper for sys_sigaction"""
        return self.sys_sigaction(signum, act, oldact)