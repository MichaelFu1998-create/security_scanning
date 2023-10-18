def define_spotsignal(self):
        """
        Identify the "expected" flux value at the time of each observation based on the 
        Kepler long-cadence data, to ensure variations observed are not the effects of a single
        large starspot. Only works if the target star was targeted for long or short cadence
        observations during the primary mission.
        """
        client = kplr.API()
        star = client.star(self.kic)

        lcs = star.get_light_curves(short_cadence=False)
        time, flux, ferr, qual = [], [], [], []
        for lc in lcs:
            with lc.open() as f:
                hdu_data = f[1].data
                time.append(hdu_data["time"])
                flux.append(hdu_data["pdcsap_flux"])
                ferr.append(hdu_data["pdcsap_flux_err"])
                qual.append(hdu_data["sap_quality"])
            tout = np.array([])
            fout = np.array([])
            eout = np.array([])
            for i in range(len(flux)):
                t = time[i][qual[i] == 0]
                f = flux[i][qual[i] == 0]
                e = ferr[i][qual[i] == 0]

                t = t[np.isfinite(f)]
                e = e[np.isfinite(f)]
                f = f[np.isfinite(f)]

                e /= np.median(f)
                f /= np.median(f)
                tout = np.append(tout, t[50:]+54833)
                fout = np.append(fout, f[50:])
                eout = np.append(eout, e[50:])

            self.spot_signal = np.zeros(52)

            for i in range(len(self.times)):
                if self.times[i] < 55000:
                    self.spot_signal[i] = 1.0
                else:
                    self.spot_signal[i] = fout[np.abs(self.times[i] - tout) == np.min(np.abs(self.times[i] - tout))]