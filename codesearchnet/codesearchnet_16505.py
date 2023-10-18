def write(self,file,optstring="",quote=False):
        """write the 'object' line; additional args are packed in string"""
        classid = str(self.id)
        if quote: classid = '"'+classid+'"'
        # Only use a *single* space between tokens; both chimera's and pymol's DX parser
        # does not properly implement the OpenDX specs and produces garbage with multiple
        # spaces. (Chimera 1.4.1, PyMOL 1.3)
        file.write('object '+classid+' class '+str(self.name)+' '+\
                   optstring+'\n')