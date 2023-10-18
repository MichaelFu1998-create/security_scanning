def DSP_callback_tic(self):
        """
        Add new tic time to the DSP_tic list. Will not be called if
        Tcapture = 0.
        
        """
        if self.Tcapture > 0:
            self.DSP_tic.append(time.time()-self.start_time)