def get_LR(self,in_data):
        """
        Splits incoming packed stereo data into separate left and right channels
        and returns an array of left samples and an array of right samples
        
        Parameters
        ----------
        in_data : input data from the streaming object in the callback function. 
        
        Returns
        -------
        left_in : array of incoming left channel samples
        right_in : array of incoming right channel samples
        
        """
        for i in range(0,self.frame_length*2):
            if i % 2:
                self.right_in[(int)(i/2)] = in_data[i]
            else:
                self.left_in[(int)(i/2)] = in_data[i]
        return self.left_in, self.right_in