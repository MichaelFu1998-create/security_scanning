def hamm_gen(self,j):
        """
        Generates parity check matrix (H) and generator
        matrix (G). 
        
        Parameters
        ----------
        j: Number of Hamming code parity bits with n = 2^j-1 and k = n-j
        
        returns
        -------
        G: Systematic generator matrix with left-side identity matrix
        H: Systematic parity-check matrix with right-side identity matrix
        R: k x k identity matrix
        n: number of total bits/block
        k: number of source bits/block
        
        Andrew Smit November 2018
        
        """
        if(j < 3):
            raise ValueError('j must be > 2')

        # calculate codeword length
        n = 2**j-1
        
        # calculate source bit length
        k = n-j
        
        # Allocate memory for Matrices
        G = np.zeros((k,n),dtype=int)
        H = np.zeros((j,n),dtype=int)
        P = np.zeros((j,k),dtype=int)
        R = np.zeros((k,n),dtype=int)
        
        # Encode parity-check matrix columns with binary 1-n
        for i in range(1,n+1):
            b = list(binary(i,j))
            for m in range(0,len(b)):
                b[m] = int(b[m])
            H[:,i-1] = np.array(b)

        # Reformat H to be systematic
        H1 = np.zeros((1,j),dtype=int)
        H2 = np.zeros((1,j),dtype=int)
        for i in range(0,j):
            idx1 = 2**i-1
            idx2 = n-i-1
            H1[0,:] = H[:,idx1]
            H2[0,:] = H[:,idx2]
            H[:,idx1] = H2
            H[:,idx2] = H1
        
        # Get parity matrix from H
        P = H[:,:k]
        
        # Use P to calcuate generator matrix P
        G[:,:k] = np.diag(np.ones(k))
        G[:,k:] = P.T
        
        # Get k x k identity matrix
        R[:,:k] = np.diag(np.ones(k))

        return G, H, R, n, k