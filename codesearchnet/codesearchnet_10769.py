def stream_stats(self):
        """
        Display basic statistics of callback execution: ideal period 
        between callbacks, average measured period between callbacks,
        and average time spent in the callback.
        
        """
        Tp = self.frame_length/float(self.fs)*1000
        print('Delay (latency) in Entering the Callback the First Time = %6.2f (ms)' \
              % (self.DSP_tic[0]*1000,))
        print('Ideal Callback period = %1.2f (ms)' % Tp)
        Tmp_mean = np.mean(np.diff(np.array(self.DSP_tic))[1:]*1000)
        print('Average Callback Period = %1.2f (ms)' % Tmp_mean)
        Tprocess_mean = np.mean(np.array(self.DSP_toc)-np.array(self.DSP_tic))*1000
        print('Average Callback process time = %1.2f (ms)' % Tprocess_mean)