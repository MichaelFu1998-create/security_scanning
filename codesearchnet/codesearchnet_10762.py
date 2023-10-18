def interactive_stream(self,Tsec = 2, numChan = 1):
        """
        Stream audio with start and stop radio buttons
        
        Interactive stream is designed for streaming audio through this object using
        a callback function. This stream is threaded, so it can be used with ipywidgets.
        Click on the "Start Streaming" button to start streaming and click on "Stop Streaming"
        button to stop streaming.

        Parameters
        ----------

        Tsec : stream time in seconds if Tsec > 0. If Tsec = 0, then stream goes to infinite 
        mode. When in infinite mode, the "Stop Streaming" radio button or Tsec.stop() can be 
        used to stop the stream.
        
        numChan : number of channels. Use 1 for mono and 2 for stereo.
        
        
        """
        self.Tsec = Tsec
        self.numChan = numChan
        self.interactiveFG = 1
        self.play = interactive(self.interaction,Stream = ToggleButtons(
                                options=['Start Streaming', 'Stop Streaming'],
                                description = ' ',
                                value = 'Stop Streaming') )
        display(self.play)