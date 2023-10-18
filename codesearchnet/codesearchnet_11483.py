def setEnvironmentalData(self, humidity, temperature):

		''' Humidity is stored as an unsigned 16 bits in 1/512%RH. The
		default value is 50% = 0x64, 0x00. As an example 48.5%
		humidity would be 0x61, 0x00.'''
		
		''' Temperature is stored as an unsigned 16 bits integer in 1/512
		degrees there is an offset: 0 maps to -25C. The default value is
		25C = 0x64, 0x00. As an example 23.5% temperature would be
		0x61, 0x00.
		The internal algorithm uses these values (or default values if
		not set by the application) to compensate for changes in
		relative humidity and ambient temperature.'''
		
		hum_perc = humidity << 1
		
		parts = math.fmod(temperature)
		fractional = parts[0]
		temperature = parts[1]

		temp_high = ((temperature + 25) << 9)
		temp_low = ((fractional / 0.001953125) & 0x1FF)
		
		temp_conv = (temp_high | temp_low)

		buf = [hum_perc, 0x00,((temp_conv >> 8) & 0xFF), (temp_conv & 0xFF)]
		
		self._device.writeList(CCS811_ENV_DATA, buf)