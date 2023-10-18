def _push(self, value):
        """
        Push into the stack

              ITEM0
              ITEM1
              ITEM2
        sp->  {empty}
        """
        assert isinstance(value, int) or isinstance(value, BitVec) and value.size == 256
        if len(self.stack) >= 1024:
            raise StackOverflow()

        if isinstance(value, int):
            value = value & TT256M1

        value = simplify(value)
        if isinstance(value, Constant) and not value.taint:
            value = value.value
        self.stack.append(value)