def conv_encoder(self,input,state):
        """
        output, state = conv_encoder(input,state)
        We get the 1/2 or 1/3 rate from self.rate
        Polys G1 and G2 are entered as binary strings, e.g,
        G1 = '111' and G2 = '101' for K = 3
        G1 = '1011011' and G2 = '1111001' for K = 7
        G3 is also included for rate 1/3
        Input state as a binary string of length K-1, e.g., '00' or '0000000' 
        e.g., state = '00' for K = 3
        e.g., state = '000000' for K = 7
        Mark Wickert and Andrew Smit 2018
        """

        output = []

        if(self.rate == Fraction(1,2)):
            for n in range(len(input)):
                u1 = int(input[n])
                u2 = int(input[n])
                for m in range(1,self.constraint_length):
                    if int(self.G_polys[0][m]) == 1: # XOR if we have a connection
                        u1 = u1 ^ int(state[m-1])
                    if int(self.G_polys[1][m]) == 1: # XOR if we have a connection
                        u2 = u2 ^ int(state[m-1])
                # G1 placed first, G2 placed second
                output = np.hstack((output, [u1, u2]))
                state = bin(int(input[n]))[-1] + state[:-1]
        elif(self.rate == Fraction(1,3)):
            for n in range(len(input)):
                if(int(self.G_polys[0][0]) == 1):
                    u1 = int(input[n])
                else:
                    u1 = 0
                if(int(self.G_polys[1][0]) == 1):
                    u2 = int(input[n])
                else:
                    u2 = 0
                if(int(self.G_polys[2][0]) == 1):
                    u3 = int(input[n])
                else:
                    u3 = 0
                for m in range(1,self.constraint_length):
                    if int(self.G_polys[0][m]) == 1: # XOR if we have a connection
                        u1 = u1 ^ int(state[m-1])
                    if int(self.G_polys[1][m]) == 1: # XOR if we have a connection
                        u2 = u2 ^ int(state[m-1])
                    if int(self.G_polys[2][m]) == 1: # XOR if we have a connection
                        u3 = u3 ^ int(state[m-1])
                # G1 placed first, G2 placed second, G3 placed third
                output = np.hstack((output, [u1, u2, u3]))
                
                state = bin(int(input[n]))[-1] + state[:-1]

        return output, state