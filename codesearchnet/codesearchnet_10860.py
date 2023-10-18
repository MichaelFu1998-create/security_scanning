def freq_resp(self, mode= 'dB', fs = 8000, ylim = [-100,2]):
        """
        Frequency response plot
        """
        iir_d.freqz_resp_cas_list([self.sos],mode,fs=fs)
        pylab.grid()
        pylab.ylim(ylim)