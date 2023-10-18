def _append_element(self, render_func, pe):
        '''
        Append a render function and the parameters to pass
        an equivilent PathElement, or the PathElement itself.
        '''
        self._render_funcs.append(render_func)
        self._elements.append(pe)