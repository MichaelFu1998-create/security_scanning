def stream(self,Tsec = 2,numChan = 1):
        """
        Stream audio using callback

        Parameters
        ----------

        Tsec : stream time in seconds if Tsec > 0. If Tsec = 0, then stream goes to infinite 
        mode. When in infinite mode, Tsec.stop() can be used to stop the stream.
        
        numChan : number of channels. Use 1 for mono and 2 for stereo.

        """
        self.Tsec = Tsec
        self.numChan = numChan
        self.N_samples = int(self.fs*Tsec)
        self.data_capture = []
        self.data_capture_left = []
        self.data_capture_right = []
        self.capture_sample_count = 0
        self.DSP_tic = []
        self.DSP_toc = []
        self.start_time = time.time()
        self.stop_stream = False
        # open stream using callback (3)
        stream = self.p.open(format=pyaudio.paInt16,
                             channels=numChan,
                             rate=self.fs,
                             input=True,
                             output=True,
                             input_device_index = self.in_idx,
                             output_device_index = self.out_idx,
                             frames_per_buffer = self.frame_length,
                             stream_callback=self.stream_callback)

        # start the stream (4)
        stream.start_stream()

        # infinite mode
        if(Tsec == 0):
            while stream.is_active():
                if self.stop_stream:
                    stream.stop_stream()
                time.sleep(self.sleep_time)
        else:
        # wait for stream to finish (5)
            while stream.is_active():
                if self.capture_sample_count >= self.N_samples:
                    stream.stop_stream()
                if self.stop_stream:
                    stream.stop_stream()
                time.sleep(self.sleep_time)

        # stop stream (6)
        stream.stop_stream()
        stream.close()

        # close PyAudio (7)
        self.p.terminate()
        self.stream_data = True
        # print('Audio input/output streaming session complete!')
        
        if(self.interactiveFG):
            # Move radio button back to 'Stop Streaming'
            self.play.children[0].value = 'Stop Streaming'
        else:
            if(self.print_when_done == 1):
                print('Completed')