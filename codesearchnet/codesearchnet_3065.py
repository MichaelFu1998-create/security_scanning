def emit(self, op_code, *args):
        ''' Adds op_code with specified args to tape '''
        self.tape.append(OP_CODES[op_code](*args))