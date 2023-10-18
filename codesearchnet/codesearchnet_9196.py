def set_calibration_data(self, scale=None, offset=None):
        """
        Set device calibration data based on settings in /etc/temper.conf.
        """
        if scale is not None and offset is not None:
            self._scale = scale
            self._offset = offset
        elif scale is None and offset is None:
            self._scale = 1.0
            self._offset = 0.0
            try:
                f = open('/etc/temper.conf', 'r')
            except IOError:
                f = None
            if f:
                lines = f.read().split('\n')
                f.close()
                for line in lines:
                    matches = re.match(CALIB_LINE_STR, line)
                    if matches:
                        bus = int(matches.groups()[0])
                        ports = matches.groups()[1]
                        scale = float(matches.groups()[2])
                        offset = float(matches.groups()[3])
                        if (str(ports) == str(self._ports)) and (str(bus) == str(self._bus)):
                            self._scale = scale
                            self._offset = offset
        else:
            raise RuntimeError("Must set both scale and offset, or neither")