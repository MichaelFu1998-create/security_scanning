def saveThing(self,thing,fname,overwrite=True,ext=".pkl"):
        """save any object as /swhlab4/ID_[fname].pkl"""
        if not os.path.exists(os.path.dirname(self.outpre)):
            os.mkdir(os.path.dirname(self.outpre))
        if ext and not ext in fname:
            fname+=ext
        fname=self.outpre+fname
        if overwrite is False:
            if os.path.exists(fname):
                print(" o- not overwriting [%s]"%os.path.basename(fname))
                return
        time1=cm.timethis()
        pickle.dump(thing, open(fname,"wb"),pickle.HIGHEST_PROTOCOL)
        print(" <- saving [%s] %s (%.01f kB) took %.02f ms"%(\
              os.path.basename(fname),str(type(thing)),
              sys.getsizeof(pickle.dumps(thing, -1))/1e3,
              cm.timethis(time1)))