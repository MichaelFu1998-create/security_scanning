def DSP_callback_toc(self):
        """
        Add new toc time to the DSP_toc list. Will not be called if
        Tcapture = 0.

        """
        if self.Tcapture > 0:
            self.DSP_toc.append(time.time()-self.start_time)