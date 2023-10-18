def bm_calc(self,ref_code_bits, rec_code_bits, metric_type, quant_level):
        """
        distance = bm_calc(ref_code_bits, rec_code_bits, metric_type)
        Branch metrics calculation

        Mark Wickert and Andrew Smit October 2018
        """
        distance = 0
        if metric_type == 'soft': # squared distance metric
            bits = binary(int(ref_code_bits),self.rate.denominator)
            for k in range(len(bits)):
                ref_bit = (2**quant_level-1)*int(bits[k],2)
                distance += (int(rec_code_bits[k]) - ref_bit)**2
        elif metric_type == 'hard': # hard decisions
            bits = binary(int(ref_code_bits),self.rate.denominator)
            for k in range(len(rec_code_bits)):
                distance += abs(rec_code_bits[k] - int(bits[k]))
        elif metric_type == 'unquant': # unquantized
            bits = binary(int(ref_code_bits),self.rate.denominator)
            for k in range(len(bits)):
                distance += (float(rec_code_bits[k])-float(bits[k]))**2
        else:
            print('Invalid metric type specified')
            raise ValueError('Invalid metric type specified. Use soft, hard, or unquant')
        return distance