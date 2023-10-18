def disassemble(self):
        """Disassemble serialized protocol buffers file.
        """
        ser_pb = open(self.input_file, 'rb').read()  # Read serialized pb file
        
        fd = FileDescriptorProto()
        fd.ParseFromString(ser_pb)
        self.name = fd.name
        
        self._print('// Reversed by pbd (https://github.com/rsc-dev/pbd)')
        self._print('syntax = "proto2";')
        self._print('')
        
        if len(fd.package) > 0:
            self._print('package {};'.format(fd.package))
            self.package = fd.package
        else:
            self._print('// Package not defined')
        
        self._walk(fd)