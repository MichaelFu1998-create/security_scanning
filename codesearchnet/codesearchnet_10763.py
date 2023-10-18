def thread_stream(self,Tsec = 2,numChan = 1):
        """
        Stream audio in a thread using callback. The stream is threaded, so widgets can be
        used simultaneously during stream.

        Parameters
        ----------

        Tsec : stream time in seconds if Tsec > 0. If Tsec = 0, then stream goes to infinite 
        mode. When in infinite mode, Tsec.stop() can be used to stop the stream.
        
        numChan : number of channels. Use 1 for mono and 2 for stereo.

        """
        def stream_thread(time,channel):
            self.stream(Tsec=time,numChan = channel)

        # Thread the streaming function
        t = Thread(target=stream_thread, args=(Tsec,numChan,))

        # Start the stream
        t.start()