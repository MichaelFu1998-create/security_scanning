def abstract_relational_comparison(self, other,
                                   self_first=True):  # todo speed up!
    ''' self<other if self_first else other<self.
       Returns the result of the question: is self smaller than other?
       in case self_first is false it returns the answer of:
                                           is other smaller than self.
       result is PyJs type: bool or undefined'''

    px = to_primitive(self, 'Number')
    py = to_primitive(other, 'Number')
    if not self_first:  # reverse order
        px, py = py, px
    if not (Type(px) == 'String' and Type(py) == 'String'):
        px, py = to_number(px), to_number(py)
        if is_nan(px) or is_nan(py):
            return None  # watch out here!
        return px < py  # same cmp algorithm
    else:
        # I am pretty sure that python has the same
        # string cmp algorithm but I have to confirm it
        return px < py