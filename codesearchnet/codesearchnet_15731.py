def call(self, args, axis=0, out=None, chunksize=1024 * 1024, **kwargs):
        """ axis is the axis to chop it off.
            if self.altreduce is set, the results will
            be reduced with altreduce and returned
            otherwise will be saved to out, then return out.
        """
        if self.altreduce is not None:
            ret = [None]
        else:
            if out is None :
                if self.outdtype is not None:
                    dtype = self.outdtype
                else:
                    try:
                        dtype = numpy.result_type(*[args[i] for i in self.ins] * 2)
                    except:
                        dtype = None
                out = sharedmem.empty(
                        numpy.broadcast(*[args[i] for i in self.ins] * 2).shape,
                        dtype=dtype)
        if axis != 0:
            for i in self.ins:
                args[i] = numpy.rollaxis(args[i], axis)
            out = numpy.rollaxis(out, axis)
        size = numpy.max([len(args[i]) for i in self.ins])
        with sharedmem.MapReduce() as pool:
            def work(i):
                sl = slice(i, i+chunksize)
                myargs = args[:]
                for j in self.ins:
                    try: 
                        tmp = myargs[j][sl]
                        a, b, c = sl.indices(len(args[j]))
                        myargs[j] = tmp
                    except Exception as e:
                        print tmp
                        print j, e
                        pass
                if b == a: return None
                rt = self.ufunc(*myargs, **kwargs)
                if self.altreduce is not None:
                    return rt
                else:
                    out[sl] = rt
            def reduce(rt):
                if self.altreduce is None:
                    return
                if ret[0] is None:
                    ret[0] = rt
                elif rt is not None:
                    ret[0] = self.altreduce(ret[0], rt)

            pool.map(work, range(0, size, chunksize), reduce=reduce)

        if self.altreduce is None:
            if axis != 0:
                out = numpy.rollaxis(out, 0, axis + 1)
            return out                
        else:
            return ret[0]