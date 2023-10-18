def snapshot(self, target, defer=True, file_number=None):
        '''
        Ask the drawqueue to output to target.

        target can be anything supported by the combination
        of canvas implementation and drawqueue implmentation.

        If target is not supported then an exception is thrown.
        '''
        output_func = self.output_closure(target, file_number)
        if defer:
            self._drawqueue.append(output_func)
        else:
            self._drawqueue.append_immediate(output_func)