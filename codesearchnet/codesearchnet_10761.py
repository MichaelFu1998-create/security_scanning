def in_out_check(self):
        """
        Checks the input and output to see if they are valid
        
        """
        devices = available_devices()
        if not self.in_idx in devices:
            raise OSError("Input device is unavailable")
        in_check = devices[self.in_idx]
        if not self.out_idx in devices:
            raise OSError("Output device is unavailable")
        out_check = devices[self.out_idx]
        if((in_check['inputs'] == 0) and (out_check['outputs']==0)):
            raise StandardError('Invalid input and output devices')
        elif(in_check['inputs'] == 0):
            raise ValueError('Selected input device has no inputs')
        elif(out_check['outputs'] == 0):
            raise ValueError('Selected output device has no outputs')
        return True