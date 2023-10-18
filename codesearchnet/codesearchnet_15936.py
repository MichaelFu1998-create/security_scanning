def strip_present(payload):
        """strip(4 byte) radiotap.present. Those are flags that
        identify existence of incoming radiotap meta-data.
        :idx: int
        :return: str
        :return: namedtuple
        """
        present = collections.namedtuple(
            'present', ['tsft', 'flags', 'rate', 'channel', 'fhss',
                        'dbm_antsignal', 'dbm_antnoise', 'lock_quality',
                        'tx_attenuation', 'db_tx_attenuation', 'dbm_tx_power',
                        'antenna', 'db_antsignal', 'db_antnoise', 'rxflags',
                        'txflags', 'rts_retries', 'data_retries', 'xchannel',
                        'mcs', 'ampdu', 'vht', 'rtap_ns', 'ven_ns', 'ext'])

        val = struct.unpack('<L', payload)[0]
        bits = format(val, '032b')[::-1]
        present.tsft = int(bits[0])               # timer synchronization function
        present.flags = int(bits[1])              # flags
        present.rate = int(bits[2])               # rate
        present.channel = int(bits[3])            # channel
        present.fhss = int(bits[4])               # frequency hoping spread spectrum
        present.dbm_antsignal = int(bits[5])      # dbm antenna signal
        present.dbm_antnoise = int(bits[6])       # dbm antenna noinse
        present.lock_quality = int(bits[7])       # quality of barker code lock
        present.tx_attenuation = int(bits[8])     # transmitter attenuation
        present.db_tx_attenuation = int(bits[9])  # decibel transmit attenuation
        present.dbm_tx_power = int(bits[10])      # dbm transmit power
        present.antenna = int(bits[11])           # antenna
        present.db_antsignal = int(bits[12])      # db antenna signal
        present.db_antnoise = int(bits[13])       # db antenna noise
        present.rxflags = int(bits[14])           # receiver flags
        present.txflags = int(bits[15])           # transmitter flags
        present.rts_retries = int(bits[16])       # rts(request to send) retries
        present.data_retries = int(bits[17])      # data retries
        present.xchannel = int(bits[18])          # xchannel
        present.mcs = int(bits[19])               # modulation and coding scheme
        present.ampdu = int(bits[20])             # aggregated mac protocol data unit
        present.vht = int(bits[21])               # very high throughput
        present.rtap_ns = int(bits[29])           # radiotap namespace
        present.ven_ns = int(bits[30])            # vendor namespace
        present.ext = int(bits[31])               # extension

        return present, bits