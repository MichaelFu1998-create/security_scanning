def sys_rt_sigprocmask(self, cpu, how, newset, oldset):
        """Wrapper for sys_sigprocmask"""
        return self.sys_sigprocmask(cpu, how, newset, oldset)