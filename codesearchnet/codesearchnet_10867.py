def cyclic_encoder(self,x,G='1011'):
        """
        Encodes input bit array x using cyclic block code.
        
        parameters
        ----------
        x: vector of source bits to be encoded by block encoder. Numpy array
           of integers expected.
        
        returns
        -------
        codewords: vector of code words generated from input vector
        
        Andrew Smit November 2018
        """
        
        # Check block length
        if(len(x) % self.k or len(x) < self.k):
            raise ValueError('Error: Incomplete block in input array. Make sure input array length is a multiple of %d' %self.k)
        
        # Check data type of input vector
        if(np.dtype(x[0]) != int):
            raise ValueError('Error: Input array should be int data type')
        
        # Calculate number of blocks
        Num_blocks = int(len(x) / self.k)
        
        codewords = np.zeros((Num_blocks,self.n),dtype=int)
        x = np.reshape(x,(Num_blocks,self.k))
        
        #print(x)
        
        for p in range(Num_blocks):
            S = np.zeros(len(self.G))
            codeword = np.zeros(self.n)
            current_block = x[p,:]
            #print(current_block)
            for i in range(0,self.n):
                if(i < self.k):
                    S[0] = current_block[i]
                    S0temp = 0
                    for m in range(0,len(self.G)):
                        if(self.G[m] == '1'):
                            S0temp = S0temp + S[m]
                            #print(j,S0temp,S[j])
                    S0temp = S0temp % 2
                    S = np.roll(S,1)
                    codeword[i] = current_block[i]
                    S[1] = S0temp
                else:
                    out = 0
                    for m in range(1,len(self.G)):
                        if(self.G[m] == '1'):
                            out = out + S[m]
                    codeword[i] = out % 2
                    S = np.roll(S,1)
                    S[1] = 0
            codewords[p,:] = codeword
            #print(codeword)
        
        codewords = np.reshape(codewords,np.size(codewords))
                
        return codewords.astype(int)