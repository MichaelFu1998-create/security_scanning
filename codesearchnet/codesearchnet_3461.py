def _init_arm_kernel_helpers(self):
        """
        ARM kernel helpers

        https://www.kernel.org/doc/Documentation/arm/kernel_user_helpers.txt
        """

        page_data = bytearray(b'\xf1\xde\xfd\xe7' * 1024)

        # Extracted from a RPi2
        preamble = binascii.unhexlify(
            'ff0300ea' +
            '650400ea' +
            'f0ff9fe5' +
            '430400ea' +
            '220400ea' +
            '810400ea' +
            '000400ea' +
            '870400ea'
        )

        # XXX(yan): The following implementations of cmpxchg and cmpxchg64 were
        # handwritten to not use any exclusive instructions (e.g. ldrexd) or
        # locking. For actual implementations, refer to
        # arch/arm64/kernel/kuser32.S in the Linux source code.
        __kuser_cmpxchg64 = binascii.unhexlify(
            '30002de9' +  # push    {r4, r5}
            '08c09de5' +  # ldr     ip, [sp, #8]
            '30009ce8' +  # ldm     ip, {r4, r5}
            '010055e1' +  # cmp     r5, r1
            '00005401' +  # cmpeq   r4, r0
            '0100a013' +  # movne   r0, #1
            '0000a003' +  # moveq   r0, #0
            '0c008c08' +  # stmeq   ip, {r2, r3}
            '3000bde8' +  # pop     {r4, r5}
            '1eff2fe1'   # bx      lr
        )

        __kuser_dmb = binascii.unhexlify(
            '5bf07ff5' +  # dmb ish
            '1eff2fe1'   # bx lr
        )

        __kuser_cmpxchg = binascii.unhexlify(
            '003092e5' +  # ldr     r3, [r2]
            '000053e1' +  # cmp     r3, r0
            '0000a003' +  # moveq   r0, #0
            '00108205' +  # streq   r1, [r2]
            '0100a013' +  # movne   r0, #1
            '1eff2fe1'   # bx      lr
        )

        # Map a TLS segment
        self._arm_tls_memory = self.current.memory.mmap(None, 4, 'rw ')

        __kuser_get_tls = binascii.unhexlify(
            '04009FE5' +  # ldr r0, [pc, #4]
            '010090e8' +  # ldm r0, {r0}
            '1eff2fe1'   # bx lr
        ) + struct.pack('<I', self._arm_tls_memory)

        tls_area = b'\x00' * 12

        version = struct.pack('<I', 5)

        def update(address, code):
            page_data[address:address + len(code)] = code

        # Offsets from Documentation/arm/kernel_user_helpers.txt in Linux
        update(0x000, preamble)
        update(0xf60, __kuser_cmpxchg64)
        update(0xfa0, __kuser_dmb)
        update(0xfc0, __kuser_cmpxchg)
        update(0xfe0, __kuser_get_tls)
        update(0xff0, tls_area)
        update(0xffc, version)

        self.current.memory.mmap(0xffff0000, len(page_data), 'r x', page_data)