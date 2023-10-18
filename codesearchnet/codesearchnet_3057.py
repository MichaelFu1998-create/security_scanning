def abstract_relational_comparison(self, other, self_first=True):
        ''' self<other if self_first else other<self.
           Returns the result of the question: is self smaller than other?
           in case self_first is false it returns the answer of:
                                               is other smaller than self.
           result is PyJs type: bool or undefined'''
        px = self.to_primitive('Number')
        py = other.to_primitive('Number')
        if not self_first:  #reverse order
            px, py = py, px
        if not (px.Class == 'String' and py.Class == 'String'):
            px, py = px.to_number(), py.to_number()
            if px.is_nan() or py.is_nan():
                return undefined
            return Js(px.value < py.value)  # same cmp algorithm
        else:
            # I am pretty sure that python has the same
            # string cmp algorithm but I have to confirm it
            return Js(px.value < py.value)