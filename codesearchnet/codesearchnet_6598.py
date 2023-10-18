def num2hex(self, num):
        '''
            Convert a decimal number to hexadecimal
        '''
        temp = ''
        for i in range(0, 4):
            x = self.hexChars[ ( num >> (i * 8 + 4) ) & 0x0F ]
            y = self.hexChars[ ( num >> (i * 8) ) & 0x0F ]
            temp += (x + y)

        return temp