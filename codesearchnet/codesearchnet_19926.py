def html_single_basic(self,ID):
        """
        generate ./swhlab/xxyxxzzz.html for a single given abf.
        Input can be an ABF file path of ABF ID.
        """
        if not ID in self.cells:
            self.log.error("ID [%s] not seen!",ID)
            return
        htmlFname=os.path.abspath(self.abfFolder2+"/"+ID+".html")
        html="<h1>Data for ID %s</h1>"%ID
        npics=0
        for childID in [os.path.splitext(x)[0] for x in self.fnamesByCell[ID]]:
            pics=[x for x in self.fnames2 if x.startswith(childID) and os.path.splitext(x)[1].lower() in [".png",".jpg"]]
            html+="<code>%s</code><br>"%(os.path.abspath(self.abfFolder+'/'+childID+".abf"))
            for i,pic in enumerate(pics):
                html+='<a href="%s"><img class="datapic" src="%s" width="200"></a>'%(pic,pic)
                npics+=1
            html+="<br><br><br>"
        style.save(html,htmlFname)
        self.log.info("created %s containing %d pictures",htmlFname,npics)