def cyclic_decoder(self,codewords):
        """
        Decodes a vector of cyclic coded codewords.
        
        parameters
        ----------
        codewords: vector of codewords to be decoded. Numpy array of integers expected.
        
        returns
        -------
        decoded_blocks: vector of decoded bits
        
        Andrew Smit November 2018
        """
        
        # Check block length
        if(len(codewords) % self.n or len(codewords) < self.n):
            raise ValueError('Error: Incomplete coded block in input array. Make sure coded input array length is a multiple of %d' %self.n)
        
        # Check input data type
        if(np.dtype(codewords[0]) != int):
            raise ValueError('Error: Input array should be int data type')
        
        # Calculate number of blocks
        Num_blocks = int(len(codewords) / self.n)
        
        decoded_blocks = np.zeros((Num_blocks,self.k),dtype=int)
        codewords = np.reshape(codewords,(Num_blocks,self.n))

        for p in range(Num_blocks):
            codeword = codewords[p,:]
            Ureg = np.zeros(self.n)
            S = np.zeros(len(self.G))
            decoded_bits = np.zeros(self.k)
            output = np.zeros(self.n)
            for i in range(0,self.n): # Switch A closed B open
                Ureg = np.roll(Ureg,1)
                Ureg[0] = codeword[i]
                S0temp = 0
                S[0] = codeword[i]
                for m in range(len(self.G)):
                    if(self.G[m] == '1'):
                        S0temp = S0temp + S[m]
                S0 = S
                S = np.roll(S,1)
                S[1] = S0temp % 2

            for i in range(0,self.n): # Switch B closed A open
                Stemp = 0
                for m in range(1,len(self.G)):
                    if(self.G[m] == '1'):
                        Stemp = Stemp + S[m]
                S = np.roll(S,1)
                S[1] = Stemp % 2
                and_out = 1
                for m in range(1,len(self.G)):
                    if(m > 1):
                        and_out = and_out and ((S[m]+1) % 2)
                    else:
                        and_out = and_out and S[m]
                output[i] = (and_out + Ureg[len(Ureg)-1]) % 2
                Ureg = np.roll(Ureg,1)
                Ureg[0] = 0
            decoded_bits = output[0:self.k].astype(int)
            decoded_blocks[p,:] = decoded_bits
        
        return np.reshape(decoded_blocks,np.size(decoded_blocks)).astype(int)