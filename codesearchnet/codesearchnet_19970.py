def abfinfo(self,printToo=False,returnDict=False):
        """show basic info about ABF class variables."""
        info="\n### ABF INFO ###\n"
        d={}
        for thingName in sorted(dir(self)):
            if thingName in ['cm','evIs','colormap','dataX','dataY',
                             'protoX','protoY']:
                continue
            if "_" in thingName:
                continue
            thing=getattr(self,thingName)
            if type(thing) is list and len(thing)>5:
                continue
            thingType=str(type(thing)).split("'")[1]
            if "method" in thingType or "neo." in thingType:
                continue
            if thingName in ["header","MT"]:
                continue
            info+="%s <%s> %s\n"%(thingName,thingType,thing)
            d[thingName]=thing
        if printToo:
            print()
            for line in info.split("\n"):
                if len(line)<3:
                    continue
                print("   ",line)
            print()
        if returnDict:
            return d
        return info