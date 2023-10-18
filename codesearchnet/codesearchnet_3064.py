def ConstructObject(self, py_obj):
        ''' note py_obj items are NOT converted to PyJs types! '''
        obj = self.NewObject()
        for k, v in py_obj.items():
            obj.put(unicode(k), v)
        return obj