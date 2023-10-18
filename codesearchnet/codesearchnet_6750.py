def check_sufficient_inputs(self):
        '''Method to an exception if none of the pairs (T, P), (T, V), or 
        (P, V) are given. '''
        if not ((self.T and self.P) or (self.T and self.V) or (self.P and self.V)):
            raise Exception('Either T and P, or T and V, or P and V are required')