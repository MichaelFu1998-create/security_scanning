def loadThing(self,fname,ext=".pkl"):
        """save any object from /swhlab4/ID_[fname].pkl"""
        if ext and not ext in fname:
            fname+=ext
        fname=self.outpre+fname
        time1=cm.timethis()
        thing = pickle.load(open(fname,"rb"))
        print(" -> loading [%s] (%.01f kB) took %.02f ms"%(\
              os.path.basename(fname),
              sys.getsizeof(pickle.dumps(thing, -1))/1e3,
              cm.timethis(time1)))
        return thing