def sys_set_thread_area(self, user_info):
        """
        Sets a thread local storage (TLS) area. Sets the base address of the GS segment.
        :rtype: int

        :param user_info: the TLS array entry set corresponds to the value of C{u_info->entry_number}.
        :return: C{0} on success.
        """
        n = self.current.read_int(user_info, 32)
        pointer = self.current.read_int(user_info + 4, 32)
        m = self.current.read_int(user_info + 8, 32)
        flags = self.current.read_int(user_info + 12, 32)
        assert n == 0xffffffff
        assert flags == 0x51  # TODO: fix
        self.current.GS = 0x63
        self.current.set_descriptor(self.current.GS, pointer, 0x4000, 'rw')
        self.current.write_int(user_info, (0x63 - 3) // 8, 32)
        return 0