def DSP_capture_add_samples(self,new_data):
        """
        Append new samples to the data_capture array and increment the sample counter
        If length reaches Tcapture, then the newest samples will be kept. If Tcapture = 0 
        then new values are not appended to the data_capture array.
        
        """
        self.capture_sample_count += len(new_data)
        if self.Tcapture > 0:
            self.data_capture = np.hstack((self.data_capture,new_data))
            if (self.Tcapture > 0) and (len(self.data_capture) > self.Ncapture):
                self.data_capture = self.data_capture[-self.Ncapture:]