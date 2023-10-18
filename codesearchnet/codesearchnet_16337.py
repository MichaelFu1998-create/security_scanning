def read_histogram(self):
        """Read and reset the histogram. The expected return is a dictionary
        containing the counts per bin, MToF for bins 1, 3, 5, and 7, temperature,
        pressure, the sampling period, the checksum, PM1, PM2.5, and PM10.

        **NOTE:** The sampling period for the OPCN1 seems to be incorrect.

        :returns: dictionary
        """
        resp = []
        data = {}

        # command byte
        command = 0x30

        # Send the command byte
        self.cnxn.xfer([command])

        # Wait 10 ms
        sleep(10e-3)

        # read the histogram
        for i in range(62):
            r = self.cnxn.xfer([0x00])[0]
            resp.append(r)

        # convert to real things and store in dictionary!
        data['Bin 0']           = self._16bit_unsigned(resp[0], resp[1])
        data['Bin 1']           = self._16bit_unsigned(resp[2], resp[3])
        data['Bin 2']           = self._16bit_unsigned(resp[4], resp[5])
        data['Bin 3']           = self._16bit_unsigned(resp[6], resp[7])
        data['Bin 4']           = self._16bit_unsigned(resp[8], resp[9])
        data['Bin 5']           = self._16bit_unsigned(resp[10], resp[11])
        data['Bin 6']           = self._16bit_unsigned(resp[12], resp[13])
        data['Bin 7']           = self._16bit_unsigned(resp[14], resp[15])
        data['Bin 8']           = self._16bit_unsigned(resp[16], resp[17])
        data['Bin 9']           = self._16bit_unsigned(resp[18], resp[19])
        data['Bin 10']          = self._16bit_unsigned(resp[20], resp[21])
        data['Bin 11']          = self._16bit_unsigned(resp[22], resp[23])
        data['Bin 12']          = self._16bit_unsigned(resp[24], resp[25])
        data['Bin 13']          = self._16bit_unsigned(resp[26], resp[27])
        data['Bin 14']          = self._16bit_unsigned(resp[28], resp[29])
        data['Bin 15']          = self._16bit_unsigned(resp[30], resp[31])
        data['Bin1 MToF']       = self._calculate_mtof(resp[32])
        data['Bin3 MToF']       = self._calculate_mtof(resp[33])
        data['Bin5 MToF']       = self._calculate_mtof(resp[34])
        data['Bin7 MToF']       = self._calculate_mtof(resp[35])
        data['Temperature']     = self._calculate_temp(resp[36:40])
        data['Pressure']        = self._calculate_pressure(resp[40:44])
        data['Sampling Period'] = self._calculate_period(resp[44:48])
        data['Checksum']        = self._16bit_unsigned(resp[48], resp[49])
        data['PM1']             = self._calculate_float(resp[50:54])
        data['PM2.5']           = self._calculate_float(resp[54:58])
        data['PM10']            = self._calculate_float(resp[58:])

        # Calculate the sum of the histogram bins
        histogram_sum = data['Bin 0'] + data['Bin 1'] + data['Bin 2']   + \
                data['Bin 3'] + data['Bin 4'] + data['Bin 5'] + data['Bin 6']   + \
                data['Bin 7'] + data['Bin 8'] + data['Bin 9'] + data['Bin 10']  + \
                data['Bin 11'] + data['Bin 12'] + data['Bin 13'] + data['Bin 14'] + \
                data['Bin 15']

        return data