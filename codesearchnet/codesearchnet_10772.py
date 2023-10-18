def pack_LR(self,left_out,right_out):
        """
        Packs separate left and right channel data into one array to output
        and returns the output.

        Parameters
        ----------
        left_out : left channel array of samples going to output
        right_out : right channel array of samples going to output

        Returns
        -------
        out : packed left and right channel array of samples
        """
        for i in range(0,self.frame_length*2):
            if i % 2:
                self.out[i] = right_out[(int)(i/2)]
            else:
                self.out[i] = left_out[(int)(i/2)]
        return self.out