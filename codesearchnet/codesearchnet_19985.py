def deleteStuff(self,ext="*",spareInfo=True,spare=["_info.pkl"]):
        """delete /swhlab4/ID_*"""
        print(" -- deleting /swhlab4/"+ext)
        for fname in sorted(glob.glob(self.outpre+ext)):
            reallyDelete=True
            for item in spare:
                if item in fname:
                    reallyDelete=False
            if reallyDelete:
                os.remove(fname)