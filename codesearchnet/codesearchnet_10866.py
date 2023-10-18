def hamm_decoder(self,codewords):
        """
        Decode hamming encoded codewords. Make sure code words are of
        the appropriate length for the object.
        
        parameters
        ---------
        codewords: bit array of codewords 
        
        returns
        -------
        decoded_bits: bit array of decoded source bits
        
        Andrew Smit November 2018
        """
        if(np.dtype(codewords[0]) != int):
            raise ValueError('Error: Invalid data type. Input must be a vector of ints')

        if(len(codewords) % self.n or len(codewords) < self.n):
            raise ValueError('Error: Invalid input vector length. Length must be a multiple of %d' %self.n)

        # Calculate the number of symbols (codewords) in the input array
        N_symbols = int(len(codewords)/self.n)
        
        # Allocate memory for decoded sourcebits
        decoded_bits = np.zeros(N_symbols*self.k)
        
        # Loop through codewords to decode one block at a time
        codewords = np.reshape(codewords,(1,len(codewords)))
        for i in range(0,N_symbols):
            
            # find the syndrome of each codeword
            S = np.matmul(self.H,codewords[:,i*self.n:(i+1)*self.n].T) % 2

            # convert binary syndrome to an integer
            bits = ''
            for m in range(0,len(S)):
                bit = str(int(S[m,:]))
                bits = bits + bit
            error_pos = int(bits,2)
            h_pos = self.H[:,error_pos-1]
            
            # Use the syndrome to find the position of an error within the block
            bits = ''
            for m in range(0,len(S)):
                bit = str(int(h_pos[m]))
                bits = bits + bit
            decoded_pos = int(bits,2)-1

            # correct error if present
            if(error_pos):
                codewords[:,i*self.n+decoded_pos] = (codewords[:,i*self.n+decoded_pos] + 1) % 2
                
            # Decode the corrected codeword
            decoded_bits[i*self.k:(i+1)*self.k] = np.matmul(self.R,codewords[:,i*self.n:(i+1)*self.n].T).T % 2
        return decoded_bits.astype(int)