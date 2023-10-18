def loadable(self, src, dst):
        """
        Determines if there's enough space to load the target database.
        """
        from fabric import state
        from fabric.task_utils import crawl

        src_task = crawl(src, state.commands)
        assert src_task, 'Unknown source role: %s' % src

        dst_task = crawl(dst, state.commands)
        assert dst_task, 'Unknown destination role: %s' % src

        # Get source database size.
        src_task()
        env.host_string = env.hosts[0]
        src_size_bytes = self.get_size()

        # Get target database size, if any.
        dst_task()
        env.host_string = env.hosts[0]
        try:
            dst_size_bytes = self.get_size()
        except (ValueError, TypeError):
            dst_size_bytes = 0

        # Get target host disk size.
        free_space_bytes = self.get_free_space()

        # Deduct existing database size, because we'll be deleting it.
        balance_bytes = free_space_bytes + dst_size_bytes - src_size_bytes
        balance_bytes_scaled, units = pretty_bytes(balance_bytes)

        viable = balance_bytes >= 0
        if self.verbose:
            print('src_db_size:', pretty_bytes(src_size_bytes))
            print('dst_db_size:', pretty_bytes(dst_size_bytes))
            print('dst_free_space:', pretty_bytes(free_space_bytes))
            print
            if viable:
                print('Viable! There will be %.02f %s of disk space left.' % (balance_bytes_scaled, units))
            else:
                print('Not viable! We would be %.02f %s short.' % (balance_bytes_scaled, units))

        return viable