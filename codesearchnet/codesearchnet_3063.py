def ConstructArray(self, py_arr):
        ''' note py_arr elems are NOT converted to PyJs types!'''
        arr = self.NewArray(len(py_arr))
        arr._init(py_arr)
        return arr