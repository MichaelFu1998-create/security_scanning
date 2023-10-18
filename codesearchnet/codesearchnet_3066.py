def compile(self, start_loc=0):
        ''' Records locations of labels and compiles the code '''
        self.label_locs = {} if self.label_locs is None else self.label_locs
        loc = start_loc
        while loc < len(self.tape):
            if type(self.tape[loc]) == LABEL:
                self.label_locs[self.tape[loc].num] = loc
                del self.tape[loc]
                continue
            loc += 1
        self.compiled = True