def DSP_capture_add_samples_stereo(self,new_data_left,new_data_right):
        """
        Append new samples to the data_capture_left array and the data_capture_right
        array and increment the sample counter. If length reaches Tcapture, then the 
        newest samples will be kept. If Tcapture = 0 then new values are not appended 
        to the data_capture array.
        
        """
        self.capture_sample_count = self.capture_sample_count + len(new_data_left) + len(new_data_right)
        if self.Tcapture > 0:
            self.data_capture_left = np.hstack((self.data_capture_left,new_data_left))
            self.data_capture_right = np.hstack((self.data_capture_right,new_data_right))
            if (len(self.data_capture_left) > self.Ncapture):
                self.data_capture_left = self.data_capture_left[-self.Ncapture:]
            if (len(self.data_capture_right) > self.Ncapture):
                self.data_capture_right = self.data_capture_right[-self.Ncapture:]